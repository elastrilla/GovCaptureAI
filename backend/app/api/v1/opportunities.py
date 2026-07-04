from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityRead,
    OpportunityScoreUpdate,
    OpportunityStatusUpdate,
    OpportunitySummary,
)


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


@router.post("/", response_model=OpportunityRead)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    db_opportunity = Opportunity(
        sam_notice_id=opportunity.sam_notice_id,
        title=opportunity.title,
        solicitation_number=opportunity.solicitation_number,
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
    opportunity.qualification_rationale = score_update.rationale

    db.commit()
    db.refresh(opportunity)

    return opportunity
