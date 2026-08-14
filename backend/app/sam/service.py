from app.core.config import settings
from app.sam.client import search_sam_live
from app.sam.client import split_filter_values
from app.schemas.sam import SamSearchRequest, SamOpportunityResult, SamSearchResponse


def search_sam_mock(search_request: SamSearchRequest) -> SamSearchResponse:
    mock_results = [
        SamOpportunityResult(
            sam_notice_id="SAM-MOCK-001",
            title="Cybersecurity Support Services",
            solicitation_number="RFP-2026-001",
            notice_type="RFP",
            agency="Department of Veterans Affairs",
            naics_code="541512",
            set_aside="SDVOSB",
            posted_date="2026-07-04",
            due_date="2026-08-04",
            summary="Cybersecurity and IT support services for a federal mission customer.",
            description="Mock opportunity for cybersecurity and IT support services.",
        ),
        SamOpportunityResult(
            sam_notice_id="SAM-MOCK-002",
            title="Cloud Migration and Infrastructure Support",
            solicitation_number="RFQ-2026-002",
            notice_type="RFQ",
            agency="Department of Defense",
            naics_code="541513",
            set_aside="Small Business",
            posted_date="2026-07-04",
            due_date="2026-08-10",
            summary="Cloud infrastructure modernization and migration support services.",
            description="Mock opportunity for cloud infrastructure modernization.",
        ),
    ]

    filtered_results = mock_results

    if search_request.keyword:
        keywords = [term.lower() for term in split_filter_values(search_request.keyword)]
        filtered_results = [
            result for result in filtered_results
            if any(
                keyword in result.title.lower()
                or keyword in (result.description or "").lower()
                for keyword in keywords
            )
        ]

    if search_request.naics_code:
        naics_codes = set(split_filter_values(search_request.naics_code))
        filtered_results = [
            result for result in filtered_results
            if result.naics_code in naics_codes
        ]

    if search_request.agency:
        agencies = [term.lower() for term in split_filter_values(search_request.agency)]
        filtered_results = [
            result for result in filtered_results
            if any(agency in (result.agency or "").lower() for agency in agencies)
        ]

    if search_request.set_aside:
        set_aside = search_request.set_aside.lower()
        filtered_results = [
            result for result in filtered_results
            if set_aside in (result.set_aside or "").lower()
        ]

    if search_request.notice_type:
        notice_types = [term.lower() for term in split_filter_values(search_request.notice_type)]
        filtered_results = [
            result for result in filtered_results
            if any(notice_type in (result.notice_type or "").lower() for notice_type in notice_types)
        ]

    filtered_results = filtered_results[: search_request.limit]

    return SamSearchResponse(
        source="mock_sam_service",
        count=len(filtered_results),
        results=filtered_results,
    )


def search_sam_opportunities(search_request: SamSearchRequest) -> SamSearchResponse:
    if settings.SAM_API_MODE.lower() == "live":
        return search_sam_live(search_request)

    return search_sam_mock(search_request)
