from app.models.company import Company
from app.models.document import Document
from app.models.opportunity import Opportunity
from app.models.proposal import Proposal
from app.schemas.proposal import ProposalDraftRead


def _clean(value: object, fallback: str = "Not provided") -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text if text else fallback


def _truncate(value: str, limit: int = 900) -> str:
    text = _clean(value, "")
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3].rstrip()}..."


def _document_evidence(documents: list[Document]) -> list[str]:
    evidence = []

    for document in documents[:5]:
        parts = [
            document.title,
            document.document_type.replace("_", " "),
            _truncate(document.content_text or document.notes or "", 260),
        ]
        evidence.append(" - ".join(part for part in parts if part))

    return evidence


def pack_notes(values: list[str] | None) -> str | None:
    if not values:
        return None
    return "\n".join(value.strip() for value in values if value and value.strip()) or None


def unpack_notes(value: str | None) -> list[str]:
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


def safe_export_filename(value: str | None, fallback: str = "proposal-draft") -> str:
    text = _clean(value, fallback).lower()
    cleaned = "".join(character if character.isalnum() else "-" for character in text)
    parts = [part for part in cleaned.split("-") if part]
    return "-".join(parts)[:80] or fallback


def build_proposal_text_export(
    proposal: Proposal,
    opportunity: Opportunity,
    company: Company | None = None,
) -> str:
    review_gaps = unpack_notes(proposal.review_gaps)
    compliance_notes = unpack_notes(proposal.compliance_notes)

    metadata = [
        "GovCaptureAI Proposal Export",
        "",
        f"Proposal: {_clean(proposal.title)}",
        f"Opportunity: {_clean(opportunity.title)}",
        f"Agency: {_clean(opportunity.agency)}",
        f"Notice Type: {_clean(opportunity.notice_type)}",
        f"Solicitation: {_clean(opportunity.solicitation_number)}",
        f"NAICS: {_clean(opportunity.naics_code)}",
        f"Set-Aside: {_clean(opportunity.set_aside)}",
        f"Due Date: {_clean(opportunity.due_date)}",
        f"Company: {_clean(company.name if company else None)}",
        f"Review Status: {_clean(proposal.review_status)}",
        f"Readiness Score: {proposal.readiness_score}/100",
        "",
        "Review Notes",
        _clean(proposal.review_notes, "No review notes recorded."),
        "",
        "Compliance Notes",
        *([f"- {note}" for note in compliance_notes] or ["- No compliance notes recorded."]),
        "",
        "Review Gaps",
        *([f"- {gap}" for gap in review_gaps] or ["- No review gaps recorded."]),
        "",
        "Draft Response",
        proposal.draft_text,
        "",
        "Export Note",
        "This draft is AI-assisted capture support and should be reviewed by the proposal team before external use.",
    ]

    return "\n".join(metadata).strip() + "\n"


def _split_rationale_section(rationale: str | None, heading: str) -> str | None:
    if not rationale:
        return None

    marker = f"{heading}:"
    if marker not in rationale:
        return None

    after_marker = rationale.split(marker, 1)[1]
    next_section = after_marker.split("\n\n", 1)[0]
    return next_section.strip() or None


def _compliance_notes(company: Company, opportunity: Opportunity, documents: list[Document]) -> list[str]:
    notes = []

    if opportunity.notice_type:
        notes.append(f"Confirm response format and evaluation criteria for {opportunity.notice_type}.")
    else:
        notes.append("Confirm the notice type and required response format before submission.")

    if opportunity.due_date:
        notes.append(f"Validate all internal review dates against the response due date: {opportunity.due_date}.")
    else:
        notes.append("Confirm the response due date before committing proposal resources.")

    if opportunity.set_aside and company.certifications:
        notes.append(f"Verify eligibility evidence for {opportunity.set_aside} using company certifications.")
    elif opportunity.set_aside:
        notes.append(f"Collect certification evidence for the {opportunity.set_aside} set-aside.")

    if not documents:
        notes.append("Attach capability statement, past performance, and key personnel evidence before final review.")

    notes.extend(
        [
            "Locate and use the government-provided response template or formatting instructions when one is required.",
            "Prepare separate Technical Proposal and Cost Proposal volumes, including labor, travel, and other direct cost assumptions as applicable.",
            "Confirm pink, red, and gold team review gates, required attachments, page limits, and submission portal instructions.",
        ]
    )

    return notes


def _review_gaps(company: Company, opportunity: Opportunity, documents: list[Document]) -> list[str]:
    gaps = []

    rationale_gaps = _split_rationale_section(opportunity.qualification_rationale, "Gaps to Review")
    if rationale_gaps:
        gaps.append(rationale_gaps)

    if not company.past_performance_summary and not any(
        document.document_type == "past_performance" for document in documents
    ):
        gaps.append("Add specific past performance examples tied to the opportunity scope.")

    if not company.differentiators:
        gaps.append("Add clear differentiators before using this draft externally.")

    if not opportunity.description:
        gaps.append("Import or paste the full opportunity description to sharpen the response.")

    return gaps or ["No major gaps identified in the current capture record."]


def generate_proposal_draft(
    company: Company,
    opportunity: Opportunity,
    documents: list[Document],
    instructions: str | None = None,
) -> ProposalDraftRead:
    evidence = _document_evidence(documents)
    strengths = _split_rationale_section(opportunity.qualification_rationale, "Strengths")
    review_gaps = _review_gaps(company, opportunity, documents)
    compliance_notes = _compliance_notes(company, opportunity, documents)

    title = f"Draft Response: {_clean(opportunity.title)}"
    executive_summary = (
        f"{company.name} is prepared to support {_clean(opportunity.agency, 'the agency')} "
        f"on {_clean(opportunity.title).lower()} by applying its capabilities in "
        f"{_clean(company.core_capabilities).lower()}. "
        f"The current capture recommendation is {_clean(opportunity.qualification_recommendation, 'unscored')} "
        f"with a fit score of {_clean(opportunity.qualification_score, 'not yet scored')}."
    )
    understanding = (
        f"The opportunity appears to require {_clean(opportunity.description, 'services described in the solicitation')} "
        f"under NAICS {_clean(opportunity.naics_code)}. "
        f"The response should address the customer mission, due date, set-aside requirements, and evidence of similar delivery."
    )
    technical_approach = (
        f"Proposed approach: align {_clean(company.name)} capabilities with the stated need, "
        f"lead with {_clean(company.differentiators, 'documented differentiators')}, "
        "and organize the solution around transition readiness, delivery controls, risk management, and measurable outcomes."
    )
    management_approach = (
        "Management approach: establish a capture-to-delivery team, confirm compliance ownership, "
        "track milestones against the solicitation due date, and use the qualification rationale as the bid/no-bid control point."
    )
    past_performance = (
        f"Relevant experience: {_clean(company.past_performance_summary)}"
        if not evidence
        else "Relevant evidence:\n" + "\n".join(f"- {item}" for item in evidence)
    )

    if strengths:
        technical_approach += f" Current qualification strengths to preserve in the response: {strengths}"

    if instructions:
        compliance_notes.append(f"User instructions for this draft: {_truncate(instructions, 300)}")

    draft_sections = [
        title,
        "",
        "Executive Summary",
        executive_summary,
        "",
        "Understanding of the Requirement",
        understanding,
        "",
        "Technical Approach",
        technical_approach,
        "",
        "Management Approach",
        management_approach,
        "",
        "Past Performance and Evidence",
        past_performance,
        "",
        "Cost Proposal Planning",
        "Develop the cost volume separately from the technical response. Validate labor categories, level of effort, travel, other direct costs, assumptions, and pricing approvals before submission.",
        "",
        "Compliance Notes",
        *[f"- {note}" for note in compliance_notes],
        "",
        "Review Gaps",
        *[f"- {gap}" for gap in review_gaps],
    ]

    return ProposalDraftRead(
        opportunity_id=opportunity.id,
        company_id=company.id,
        title=title,
        executive_summary=executive_summary,
        understanding=understanding,
        technical_approach=technical_approach,
        management_approach=management_approach,
        past_performance=past_performance,
        compliance_notes=compliance_notes,
        review_gaps=review_gaps,
        draft_text="\n".join(draft_sections),
    )
