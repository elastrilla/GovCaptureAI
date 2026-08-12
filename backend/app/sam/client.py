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


def _first_non_empty(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _safe_get(data: dict, *keys, default=None):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    return current if current is not None else default


def _extract_opportunities_data(data: dict) -> list[dict]:
    candidates = (
        data.get("opportunitiesData"),
        data.get("opportunities"),
        data.get("data"),
        data.get("results"),
    )

    for candidate in candidates:
        if isinstance(candidate, list):
            return candidate

    return []


def _infer_notice_type(*values):
    text = " ".join(str(value) for value in values if value).upper()

    if "SOURCES SOUGHT" in text or "SOURCE SOUGHT" in text:
        return "Sources Sought"

    for notice_type in ("RFI", "RFQ", "RFP"):
        if notice_type in text.replace("_", "-").replace("/", "-").split("-"):
            return notice_type
        if f" {notice_type} " in f" {text} ":
            return notice_type

    return None


def _build_short_summary(
    title: str | None,
    agency: str | None,
    notice_type: str | None,
    description: str | None,
) -> str:
    description_text = str(description or "").strip()
    if description_text and not description_text.startswith("http"):
        normalized = " ".join(description_text.split())
        return normalized[:277] + "..." if len(normalized) > 280 else normalized

    parts = [
        f"{notice_type} opportunity" if notice_type else "Opportunity",
        f"for {title}" if title else None,
        f"from {agency}" if agency else None,
    ]

    return " ".join(part for part in parts if part) + "."


def parse_sam_opportunity(item: dict) -> SamOpportunityResult:
    notice_id = _first_non_empty(
        item.get("noticeId"),
        item.get("notice_id"),
        item.get("id"),
        item.get("solicitationNumber"),
        "UNKNOWN-NOTICE-ID",
    )

    title = _first_non_empty(
        item.get("title"),
        item.get("opportunityTitle"),
        _safe_get(item, "title", "value"),
        "Untitled SAM.gov Opportunity",
    )

    solicitation_number = _first_non_empty(
        item.get("solicitationNumber"),
        item.get("solicitation_number"),
        _safe_get(item, "solicitation", "number"),
    )

    notice_type = _first_non_empty(
        item.get("type"),
        item.get("noticeType"),
        item.get("notice_type"),
        item.get("typeOfNotice"),
        item.get("opportunityType"),
        _safe_get(item, "notice", "type"),
        _safe_get(item, "classification", "noticeType"),
        _infer_notice_type(
            item.get("solicitationNumber"),
            item.get("solicitation_number"),
            item.get("title"),
            item.get("opportunityTitle"),
            item.get("description"),
            item.get("synopsis"),
        ),
    )

    agency = _first_non_empty(
        item.get("fullParentPathName"),
        item.get("department"),
        item.get("subTier"),
        item.get("office"),
        _safe_get(item, "organizationHierarchy", "department", "name"),
        _safe_get(item, "organizationHierarchy", "topLevelAgency", "name"),
    )

    naics_code = _first_non_empty(
        item.get("naicsCode"),
        item.get("naics"),
        _safe_get(item, "classification", "naicsCode"),
        _safe_get(item, "classification", "naics", "code"),
    )

    set_aside = _first_non_empty(
        _safe_get(item, "typeOfSetAside", "description"),
        item.get("typeOfSetAsideDescription"),
        item.get("setAside"),
        item.get("typeOfSetAside"),
    )

    posted_date = _first_non_empty(
        item.get("postedDate"),
        item.get("posted_date"),
        _safe_get(item, "dates", "posted"),
    )

    due_date = _first_non_empty(
        item.get("responseDeadLine"),
        item.get("responseDeadline"),
        item.get("dueDate"),
        item.get("archiveDate"),
        _safe_get(item, "dates", "responseDeadline"),
    )

    description = _first_non_empty(
        item.get("description"),
        item.get("synopsis"),
        item.get("additionalInfoLink"),
        item.get("uiLink"),
        _safe_get(item, "links", "ui"),
        _safe_get(item, "links", "details"),
    )

    summary = _build_short_summary(title, agency, notice_type, description)

    return SamOpportunityResult(
        sam_notice_id=str(notice_id),
        title=str(title),
        solicitation_number=solicitation_number,
        notice_type=notice_type,
        agency=agency,
        naics_code=str(naics_code) if naics_code is not None else None,
        set_aside=set_aside,
        posted_date=posted_date,
        due_date=due_date,
        summary=summary,
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
    raw_results = _extract_opportunities_data(data)

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

    if search_request.notice_type:
        notice_type_filter = search_request.notice_type.lower()
        parsed_results = [
            result for result in parsed_results
            if notice_type_filter in (result.notice_type or "").lower()
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
