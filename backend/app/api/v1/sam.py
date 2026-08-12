from datetime import date, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db
from app.models.opportunity import Opportunity
from app.sam.client import test_sam_api_connection
from app.sam.service import search_sam_opportunities
from app.schemas.sam import SamSearchRequest, SamSearchResponse


router = APIRouter(prefix="/sam", tags=["SAM.gov"])


def _is_award_notice(notice_type: str | None) -> bool:
    return "award" in (notice_type or "").lower()


def _parse_sam_date(value):
    if not value:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        candidates = (
            "%m/%d/%Y",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%m/%d/%Y %H:%M:%S",
        )

        for format_string in candidates:
            try:
                parsed = datetime.strptime(value, format_string)
            except ValueError:
                continue

            return parsed.date()

        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None

    return None


def _build_opportunity_from_result(result):
    return Opportunity(
        sam_notice_id=result.sam_notice_id,
        title=result.title,
        solicitation_number=result.solicitation_number,
        notice_type=result.notice_type,
        agency=result.agency,
        naics_code=result.naics_code,
        set_aside=result.set_aside,
        posted_date=_parse_sam_date(result.posted_date),
        due_date=_parse_sam_date(result.due_date),
        status="new",
        summary=result.summary,
        description=result.description,
    )


def _save_sam_search_results(db: Session, search_response: SamSearchResponse):
    saved_count = 0
    skipped_count = 0
    skipped_award_count = 0
    saved_opportunities = []

    with db.begin():
        for result in search_response.results:
            if _is_award_notice(result.notice_type):
                skipped_award_count += 1
                continue

            existing = (
                db.query(Opportunity)
                .filter(Opportunity.sam_notice_id == result.sam_notice_id)
                .first()
            )

            if existing:
                skipped_count += 1
                continue

            db_opportunity = _build_opportunity_from_result(result)

            db.add(db_opportunity)
            db.flush()
            saved_count += 1
            saved_opportunities.append(
                {
                    "id": db_opportunity.id,
                    "sam_notice_id": db_opportunity.sam_notice_id,
                    "title": db_opportunity.title,
                }
            )

    return {
        "source": search_response.source,
        "matched_count": search_response.count,
        "saved_count": saved_count,
        "skipped_existing_count": skipped_count,
        "skipped_award_notice_count": skipped_award_count,
        "saved_opportunities": saved_opportunities,
    }


@router.get("/test")
def sam_test():
    return {
        "status": "ok",
        "service": "SAM.gov search module",
        "mode": settings.SAM_API_MODE,
    }


@router.get("/live-test")
def sam_live_test():
    return test_sam_api_connection()


@router.post("/search", response_model=SamSearchResponse)
def sam_search(search_request: SamSearchRequest):
    return search_sam_opportunities(search_request)


@router.post("/search/save")
def sam_search_and_save(
    search_request: SamSearchRequest,
    db: Session = Depends(get_db),
):
    search_response = search_sam_opportunities(search_request)
    return _save_sam_search_results(db, search_response)
