from app.schemas.sam import SamSearchRequest, SamOpportunityResult, SamSearchResponse


def search_sam_opportunities(search_request: SamSearchRequest) -> SamSearchResponse:
    mock_results = [
        SamOpportunityResult(
            sam_notice_id="SAM-MOCK-001",
            title="Cybersecurity Support Services",
            solicitation_number="RFP-2026-001",
            agency="Department of Veterans Affairs",
            naics_code="541512",
            set_aside="SDVOSB",
            posted_date="2026-07-04",
            due_date="2026-08-04",
            description="Mock opportunity for cybersecurity and IT support services.",
        ),
        SamOpportunityResult(
            sam_notice_id="SAM-MOCK-002",
            title="Cloud Migration and Infrastructure Support",
            solicitation_number="RFQ-2026-002",
            agency="Department of Defense",
            naics_code="541513",
            set_aside="Small Business",
            posted_date="2026-07-04",
            due_date="2026-08-10",
            description="Mock opportunity for cloud infrastructure modernization.",
        ),
    ]

    filtered_results = mock_results

    if search_request.keyword:
        keyword = search_request.keyword.lower()
        filtered_results = [
            result for result in filtered_results
            if keyword in result.title.lower()
            or keyword in (result.description or "").lower()
        ]

    if search_request.naics_code:
        filtered_results = [
            result for result in filtered_results
            if result.naics_code == search_request.naics_code
        ]

    if search_request.agency:
        agency = search_request.agency.lower()
        filtered_results = [
            result for result in filtered_results
            if agency in (result.agency or "").lower()
        ]

    if search_request.set_aside:
        set_aside = search_request.set_aside.lower()
        filtered_results = [
            result for result in filtered_results
            if set_aside in (result.set_aside or "").lower()
        ]

    return SamSearchResponse(
        source="mock_sam_service",
        count=len(filtered_results),
        results=filtered_results,
    )
