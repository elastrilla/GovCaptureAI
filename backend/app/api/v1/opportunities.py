from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.config import settings
from app.models.company import Company
from app.models.document import Document
from app.models.opportunity import Opportunity
from app.models.proposal import Proposal
from app.schemas.opportunity import (
    OpportunityAutoScoreRequest,
    OpportunityCreate,
    OpportunityRead,
    OpportunityScoreUpdate,
    OpportunityStatusUpdate,
    OpportunitySummary,
)
from app.schemas.proposal import (
    ProposalDraftRead,
    ProposalDraftRequest,
    ProposalRead,
    ProposalReviewUpdate,
)
from app.services.proposal import (
    build_proposal_text_export,
    generate_proposal_draft,
    pack_notes,
    safe_export_filename,
    unpack_notes,
)
from app.services.qualification import generate_qualification_assessment
from app.services import llm_client


router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


VALID_STATUSES = {
    "new",
    "reviewing",
    "pursuing",
    "no_bid",
    "drafting",
    "submitted",
    "won",
    "lost",
    "closed",
}

VALID_PROPOSAL_REVIEW_STATUSES = {
    "draft_generated",
    "in_review",
    "revisions_needed",
    "ready_for_final",
    "final_review",
    "submitted",
}


def _is_award_notice(opportunity: Opportunity) -> bool:
    return "award" in (opportunity.notice_type or "").lower()


def _proposal_to_read(proposal: Proposal) -> ProposalRead:
    return ProposalRead(
        id=proposal.id,
        opportunity_id=proposal.opportunity_id,
        company_id=proposal.company_id,
        title=proposal.title,
        draft_text=proposal.draft_text,
        review_status=proposal.review_status,
        readiness_score=proposal.readiness_score,
        review_notes=proposal.review_notes,
        compliance_notes=unpack_notes(proposal.compliance_notes),
        review_gaps=unpack_notes(proposal.review_gaps),
        created_at=proposal.created_at,
        updated_at=proposal.updated_at,
    )


@router.post("/", response_model=OpportunityRead)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    db_opportunity = Opportunity(
        sam_notice_id=opportunity.sam_notice_id,
        title=opportunity.title,
        solicitation_number=opportunity.solicitation_number,
        notice_type=opportunity.notice_type,
        agency=opportunity.agency,
        naics_code=opportunity.naics_code,
        set_aside=opportunity.set_aside,
        posted_date=opportunity.posted_date,
        due_date=opportunity.due_date,
        status=opportunity.status,
        description=opportunity.description,
    )

    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)

    return db_opportunity


@router.get("/", response_model=list[OpportunityRead])
def list_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).order_by(Opportunity.id).all()


@router.get("/summary", response_model=OpportunitySummary)
def get_opportunity_summary(db: Session = Depends(get_db)):
    total = db.query(Opportunity).count()

    status_counts = {
        status: db.query(Opportunity).filter(Opportunity.status == status).count()
        for status in VALID_STATUSES
    }

    average_score = (
        db.query(func.avg(Opportunity.qualification_score))
        .filter(Opportunity.qualification_score.isnot(None))
        .scalar()
    )


@router.post("/demo/reset")
def reset_demo_queue(db: Session = Depends(get_db)):
    """Reset demo capture records without touching company evidence."""
    if not settings.DEMO_RESET_ENABLED:
        raise HTTPException(status_code=404, detail="Demo queue reset is not enabled")

    proposal_count = db.query(Proposal).delete(synchronize_session=False)
    opportunity_count = db.query(Opportunity).delete(synchronize_session=False)
    db.commit()

    return {
        "message": "Demo review queue reset",
        "deleted_opportunities": opportunity_count,
        "deleted_proposals": proposal_count,
    }

    return OpportunitySummary(
        total=total,
        new=status_counts["new"],
        reviewing=status_counts["reviewing"],
        pursuing=status_counts["pursuing"],
        no_bid=status_counts["no_bid"],
        drafting=status_counts["drafting"],
        submitted=status_counts["submitted"],
        won=status_counts["won"],
        lost=status_counts["lost"],
        closed=status_counts["closed"],
        average_score=float(average_score) if average_score is not None else None,
    )


@router.get("/{opportunity_id}", response_model=OpportunityRead)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return opportunity


@router.patch("/{opportunity_id}/status", response_model=OpportunityRead)
def update_opportunity_status(
    opportunity_id: int,
    status_update: OpportunityStatusUpdate,
    db: Session = Depends(get_db),
):
    new_status = status_update.status.lower()

    if new_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid status",
                "valid_statuses": sorted(VALID_STATUSES),
            },
        )

    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opportunity.status = new_status

    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.post("/{opportunity_id}/score", response_model=OpportunityRead)
def score_opportunity(
    opportunity_id: int,
    score_update: OpportunityScoreUpdate,
    db: Session = Depends(get_db),
):
    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    opportunity.qualification_score = score_update.score
    opportunity.qualification_recommendation = score_update.recommendation
    opportunity.qualification_rationale = score_update.rationale

    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.post("/{opportunity_id}/score/auto", response_model=OpportunityRead)
def auto_score_opportunity(
    opportunity_id: int,
    score_request: OpportunityAutoScoreRequest,
    db: Session = Depends(get_db),
):
    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    if _is_award_notice(opportunity):
        raise HTTPException(
            status_code=400,
            detail="Award Notices are informational and are not eligible for qualification scoring",
        )

    company = (
        db.query(Company)
        .filter(Company.id == score_request.company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    documents = (
        db.query(Document)
        .filter(Document.company_id == company.id)
        .order_by(Document.id)
        .all()
    )

    score, recommendation, rationale = generate_qualification_assessment(
        company,
        opportunity,
        documents,
    )

    llm_rationale = llm_client.chat(
        f"Opportunity: {opportunity.title}\n"
        f"Agency: {opportunity.agency}\n"
        f"NAICS: {opportunity.naics_code}\n"
        f"Rule-based score: {score}/10\n"
        f"Recommendation: {recommendation}\n"
        f"Initial rationale: {rationale}\n\n"
        "Rewrite the rationale in clear, professional language for a government contractor. "
        "Keep it under 150 words.",
        backend="claude_fast",
        rag_enabled=True,
        system=(
            "You are a government contracting capture advisor. "
            "Write concise, actionable bid/no-bid rationale."
        ),
    )
    if llm_rationale:
        rationale = llm_rationale

    opportunity.qualification_score = score
    opportunity.qualification_recommendation = recommendation
    opportunity.qualification_rationale = rationale

    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.post("/{opportunity_id}/proposal/draft", response_model=ProposalDraftRead)
def draft_proposal_response(
    opportunity_id: int,
    draft_request: ProposalDraftRequest,
    db: Session = Depends(get_db),
):
    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    company = (
        db.query(Company)
        .filter(Company.id == draft_request.company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    documents = (
        db.query(Document)
        .filter(Document.company_id == company.id)
        .order_by(Document.id)
        .all()
    )

    draft = generate_proposal_draft(
        company,
        opportunity,
        documents,
        draft_request.instructions,
    )

    instructions_clause = (
        f"\nAdditional instructions: {draft_request.instructions}"
        if draft_request.instructions
        else ""
    )
    llm_draft_text = llm_client.chat(
        f"Opportunity: {opportunity.title}\n"
        f"Agency: {opportunity.agency}\n"
        f"NAICS: {opportunity.naics_code}\n"
        f"Description: {(opportunity.description or '')[:600]}\n"
        f"Company: {company.name}\n"
        f"Capabilities: {company.core_capabilities or 'Not specified'}\n"
        f"Differentiators: {company.differentiators or 'Not specified'}\n"
        f"Qualification score: {opportunity.qualification_score}/10 — "
        f"{opportunity.qualification_recommendation}\n"
        f"Rationale: {opportunity.qualification_rationale or ''}{instructions_clause}\n\n"
        "Write a professional proposal draft with the following sections: "
        "Executive Summary, Understanding of the Requirement, Technical Approach, "
        "Management Approach, Past Performance. Use clear government contracting language.",
        backend="claude_best",
        rag_enabled=True,
        context_k=8,
        system=(
            "You are an expert government proposal writer. "
            "Write compelling, compliant proposal sections tailored to the opportunity. "
            "Be specific, professional, and concise."
        ),
    )
    if llm_draft_text:
        draft = draft.model_copy(update={"draft_text": llm_draft_text})

    proposal = Proposal(
        opportunity_id=opportunity.id,
        company_id=company.id,
        title=draft.title,
        draft_text=draft.draft_text,
        review_status="draft_generated",
        readiness_score=30,
        compliance_notes=pack_notes(draft.compliance_notes),
        review_gaps=pack_notes(draft.review_gaps),
    )

    db.add(proposal)
    opportunity.status = "drafting"
    db.commit()
    db.refresh(proposal)

    return draft.model_copy(
        update={
            "id": proposal.id,
            "review_status": proposal.review_status,
            "readiness_score": proposal.readiness_score,
            "review_notes": proposal.review_notes,
            "created_at": proposal.created_at,
            "updated_at": proposal.updated_at,
        }
    )


@router.get("/{opportunity_id}/proposal/latest", response_model=ProposalRead)
def get_latest_proposal(
    opportunity_id: int,
    db: Session = Depends(get_db),
):
    proposal = (
        db.query(Proposal)
        .filter(Proposal.opportunity_id == opportunity_id)
        .order_by(Proposal.id.desc())
        .first()
    )

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal draft not found")

    return _proposal_to_read(proposal)


@router.get("/{opportunity_id}/proposal/{proposal_id}/export", response_class=PlainTextResponse)
def export_proposal(
    opportunity_id: int,
    proposal_id: int,
    db: Session = Depends(get_db),
):
    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id, Proposal.opportunity_id == opportunity_id)
        .first()
    )

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal draft not found")

    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    company = (
        db.query(Company)
        .filter(Company.id == proposal.company_id)
        .first()
    )

    filename = f"{safe_export_filename(opportunity.title)}-proposal-export.txt"
    return PlainTextResponse(
        build_proposal_text_export(proposal, opportunity, company),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.patch("/{opportunity_id}/proposal/{proposal_id}/review", response_model=ProposalRead)
def update_proposal_review(
    opportunity_id: int,
    proposal_id: int,
    review_update: ProposalReviewUpdate,
    db: Session = Depends(get_db),
):
    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id, Proposal.opportunity_id == opportunity_id)
        .first()
    )

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal draft not found")

    update_data = review_update.model_dump(exclude_unset=True)

    if "review_status" in update_data and update_data["review_status"] is not None:
        review_status = update_data["review_status"].lower()
        if review_status not in VALID_PROPOSAL_REVIEW_STATUSES:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid proposal review status",
                    "valid_statuses": sorted(VALID_PROPOSAL_REVIEW_STATUSES),
                },
            )
        proposal.review_status = review_status

    if "readiness_score" in update_data and update_data["readiness_score"] is not None:
        proposal.readiness_score = update_data["readiness_score"]

    if "review_notes" in update_data:
        proposal.review_notes = update_data["review_notes"]

    if "review_gaps" in update_data and update_data["review_gaps"] is not None:
        proposal.review_gaps = pack_notes(update_data["review_gaps"])

    opportunity = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id)
        .first()
    )

    if opportunity and proposal.review_status == "submitted":
        opportunity.status = "submitted"
    elif opportunity and proposal.review_status in {"ready_for_final", "final_review"}:
        opportunity.status = "drafting"

    db.commit()
    db.refresh(proposal)

    return _proposal_to_read(proposal)
