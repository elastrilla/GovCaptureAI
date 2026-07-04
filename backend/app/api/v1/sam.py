from fastapi import APIRouter

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
