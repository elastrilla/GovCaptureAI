from datetime import date, timedelta

import requests

from app.core.config import settings
from app.schemas.sam import SamSearchRequest, SamOpportunityResult, SamSearchResponse


def _default_posted_dates() -> tuple[str, str]:
    posted_to = date.today()
    posted_from = posted_to - timedelta(days=30)

    return (
        posted_from.strftime("%m/%d/%Y"),
        posted_to.strftime("%m/%d/%Y"),
    )


def _safe_get(data: dict, *keys, default=None):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    return current if current is not None else default


def parse_sam_opportunity(item: dict) -> SamOpportunityResult:
    notice_id = (
        item.get("noticeId")
        or item.get("notice_id")
        or item.get("id")
        or item.get("solicitationNumber")
        or "UNKNOWN-NOTICE-ID"
    )

    title = (
        item.get("title")
        or item.get("opportunityTitle")
        or "Untitled SAM.gov Opportunity"
    )

    solicitation_number = (
        item.get("solicitationNumber")
        or item.get("solicitation_number")
    )

    agency = (
        item.get("fullParentPathName")
        or item.get("department")
        or item.get("subTier")
        or item.get("office")
        or _safe_get(item, "organizationHierarchy", "department", "name")
    )

    naics_code = (
        item.get("naicsCode")
        or item.get("naics")
        or _safe_get(item, "classification", "naicsCode")
    )

    set_aside = (
        item.get("typeOfSetAside")
        or item.get("typeOfSetAsideDescription")
        or item.get("setAside")
    )

    posted_date = (
        item.get("postedDate")
        or item.get("posted_date")
    )

    due_date = (
        item.get("responseDeadLine")
        or item.get("responseDeadline")
        or item.get("dueDate")
        or item.get("archiveDate")
    )

    description = (
        item.get("description")
        or item.get("synopsis")
        or item.get("additionalInfoLink")
        or item.get("uiLink")
    )

    return SamOpportunityResult(
        sam_notice_id=str(notice_id),
        title=str(title),
        solicitation_number=solicitation_number,
        agency=agency,
        naics_code=str(naics_code) if naics_code is not None else None,
        set_aside=set_aside,
        posted_date=posted_date,
        due_date=due_date,
        description=description,
    )


def search_sam_live(search_request: SamSearchRequest) -> SamSearchResponse:
    if not settings.SAM_API_KEY:
        return SamSearchResponse(
            source="sam_gov_live_error",
            count=0,
            results=[],
        )

    default_posted_from, default_posted_to = _default_posted_dates()

    params = {
        "api_key": settings.SAM_API_KEY,
        "limit": search_request.limit,
        "offset": 0,
        "postedFrom": search_request.posted_from or default_posted_from,
        "postedTo": search_request.posted_to or default_posted_to,
    }

    if search_request.keyword:
        params["title"] = search_request.keyword

    if search_request.naics_code:
        params["ncode"] = search_request.naics_code

    if search_request.set_aside:
        params["typeOfSetAside"] = search_request.set_aside

    response = requests.get(
        settings.SAM_API_BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    raw_results = data.get("opportunitiesData", [])

    parsed_results = [
        parse_sam_opportunity(item)
        for item in raw_results
    ]

    if search_request.agency:
        agency_filter = search_request.agency.lower()
        parsed_results = [
            result for result in parsed_results
            if agency_filter in (result.agency or "").lower()
        ]

    return SamSearchResponse(
        source="sam_gov_live",
        count=len(parsed_results),
        results=parsed_results,
    )


def test_sam_api_connection():
    default_posted_from, default_posted_to = _default_posted_dates()

    params = {
        "api_key": settings.SAM_API_KEY,
        "limit": 1,
        "offset": 0,
        "postedFrom": default_posted_from,
        "postedTo": default_posted_to,
    }

    try:
        response = requests.get(
            settings.SAM_API_BASE_URL,
            params=params,
            timeout=20,
        )

        return {
            "status": "ok" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "url_tested": settings.SAM_API_BASE_URL,
            "mode": settings.SAM_API_MODE,
            "posted_from": default_posted_from,
            "posted_to": default_posted_to,
            "response_preview": response.text[:1000],
        }

    except requests.RequestException as error:
        return {
            "status": "error",
            "message": str(error),
        }
