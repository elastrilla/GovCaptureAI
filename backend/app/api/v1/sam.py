from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.opportunity import Opportunity
from app.sam.service import search_sam_opportunities
from app.schemas.sam import SamSearchRequest, SamSearchResponse


router = APIRouter(prefix="/sam", tags=["SAM.gov"])


@router.get("/test")
def sam_test():
    return {
        "status": "ok",
        "service": "SAM.gov search module",
        "mode": "mock",
    }


@router.post("/search", response_model=SamSearchResponse)
def sam_search(search_request: SamSearchRequest):
    return search_sam_opportunities(search_request)


@router.post("/search/save")
def sam_search_and_save(
    search_request: SamSearchRequest,
    db: Session = Depends(get_db),
):
    search_response = search_sam_opportunities(search_request)

    saved_count = 0
    skipped_count = 0
    saved_opportunities = []

    for result in search_response.results:
        existing = (
            db.query(Opportunity)
            .filter(Opportunity.sam_notice_id == result.sam_notice_id)
            .first()
        )

        if existing:
            skipped_count += 1
            continue

        db_opportunity = Opportunity(
            sam_notice_id=result.sam_notice_id,
            title=result.title,
            solicitation_number=result.solicitation_number,
            agency=result.agency,
            naics_code=result.naics_code,
            set_aside=result.set_aside,
            posted_date=result.posted_date,
            due_date=result.due_date,
            status="new",
            description=result.description,
        )

        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)

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
        "saved_opportunities": saved_opportunities,
    }
