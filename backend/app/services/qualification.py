from __future__ import annotations

import re

from app.models.company import Company
from app.models.document import Document
from app.models.opportunity import Opportunity


def _split_terms(value: str | None) -> set[str]:
    if not value:
        return set()

    return {
        part.strip().lower()
        for part in re.split(r"[,\n;/|]+", value)
        if part.strip()
    }


def _tokenize_text(value: str | None) -> set[str]:
    if not value:
        return set()

    return {
        token
        for token in re.findall(r"[a-z0-9]{4,}", value.lower())
        if token not in {"with", "from", "that", "this", "have", "your", "their"}
    }


def _set_aside_matches(company: Company, opportunity: Opportunity) -> tuple[bool, str | None]:
    if not opportunity.set_aside:
        return False, None

    set_aside = opportunity.set_aside.lower()
    certifications = " ".join(
        filter(
            None,
            [
                company.certifications,
                company.differentiators,
            ],
        )
    ).lower()

    match_rules = [
        (("8(a)", "8a"), ("8(a)", "8a")),
        (("hubzone",), ("hubzone",)),
        (("sdvosb", "service disabled veteran"), ("sdvosb", "service disabled veteran")),
        (("wosb", "woman owned"), ("wosb", "woman owned")),
        (("small business",), ("small business", "sba")),
    ]

    for opportunity_terms, company_terms in match_rules:
        if any(term in set_aside for term in opportunity_terms) and any(
            term in certifications for term in company_terms
        ):
            return True, f"set-aside alignment found for {opportunity.set_aside}"

    return False, None


def _recommendation_from_score(score: int) -> str:
    if score >= 8:
        return "pursue"
    if score >= 5:
        return "consider"
    return "no_bid"


def _build_decision_summary(score: int, recommendation: str) -> str:
    if recommendation == "pursue":
        return (
            f"Recommendation: Pursue. The opportunity shows strong alignment with the company's"
            f" capabilities and supporting evidence, resulting in a GovCaptureAI fit score of {score}/10."
        )
    if recommendation == "consider":
        return (
            f"Recommendation: Consider. The opportunity has partial alignment, but it needs a quick"
            f" capture review before committing, with a GovCaptureAI fit score of {score}/10."
        )
    return (
        f"Recommendation: No-bid. Current qualification evidence is too limited or misaligned to"
        f" justify pursuit confidently, resulting in a GovCaptureAI fit score of {score}/10."
    )


def generate_qualification_assessment(
    company: Company,
    opportunity: Opportunity,
    documents: list[Document],
) -> tuple[int, str, str]:
    score = 1
    strengths: list[str] = []
    gaps: list[str] = []

    company_naics = _split_terms(company.target_naics_codes)
    if opportunity.naics_code and opportunity.naics_code.lower() in company_naics:
        score += 3
        strengths.append(f"NAICS match on {opportunity.naics_code}")
    elif opportunity.naics_code:
        gaps.append(f"no target NAICS match was found for {opportunity.naics_code}")

    target_agencies = _split_terms(company.target_agencies)
    if opportunity.agency and any(
        agency_term in opportunity.agency.lower() or opportunity.agency.lower() in agency_term
        for agency_term in target_agencies
    ):
        score += 2
        strengths.append(f"agency match with {opportunity.agency}")
    elif opportunity.agency:
        gaps.append(f"target agency coverage is not yet clear for {opportunity.agency}")

    set_aside_match, set_aside_reason = _set_aside_matches(company, opportunity)
    if set_aside_match:
        score += 1
        strengths.append(set_aside_reason)
    elif opportunity.set_aside:
        gaps.append(f"set-aside evidence is not clearly aligned for {opportunity.set_aside}")

    evidence_text = " ".join(
        filter(
            None,
            [
                company.core_capabilities,
                company.past_performance_summary,
                company.description,
                *(document.content_text for document in documents if document.content_text),
                *(document.notes for document in documents if document.notes),
                *(document.title for document in documents if document.title),
            ],
        )
    )

    opportunity_text = " ".join(
        filter(
            None,
            [
                opportunity.title,
                opportunity.description,
                opportunity.agency,
            ],
        )
    )

    shared_keywords = sorted(_tokenize_text(evidence_text) & _tokenize_text(opportunity_text))
    if shared_keywords:
        score += 2
        strengths.append(
            "capability overlap found in "
            + ", ".join(shared_keywords[:5])
        )
    else:
        gaps.append("capability overlap in the current evidence set is limited")

    past_performance_docs = [
        document for document in documents if document.document_type == "past_performance"
    ]
    if company.past_performance_summary or past_performance_docs:
        score += 1
        strengths.append("past performance evidence is available")
    else:
        gaps.append("past performance support is still missing")

    capability_docs = [
        document for document in documents if document.document_type == "capability_statement"
    ]
    if capability_docs:
        score += 1
        strengths.append("capability statement is available for qualification review")
    else:
        gaps.append("no capability statement has been added yet")

    score = max(1, min(score, 10))
    recommendation = _recommendation_from_score(score)

    sections = [_build_decision_summary(score, recommendation)]
    if strengths:
        sections.append("Strengths: " + "; ".join(strengths[:6]) + ".")
    if gaps:
        sections.append("Gaps to Review: " + "; ".join(gaps[:3]) + ".")

    if not strengths:
        sections.append(
            "Strengths: limited fit evidence was available, so the score remains conservative."
        )

    rationale = "\n\n".join(sections)

    return score, recommendation, rationale
