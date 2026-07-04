from pydantic import BaseModel


class SamSearchRequest(BaseModel):
    keyword: str | None = None
    naics_code: str | None = None
    agency: str | None = None
    set_aside: str | None = None


class SamOpportunityResult(BaseModel):
    sam_notice_id: str
    title: str
    solicitation_number: str | None = None
    agency: str | None = None
    naics_code: str | None = None
    set_aside: str | None = None
    posted_date: str | None = None
    due_date: str | None = None
    description: str | None = None


class SamSearchResponse(BaseModel):
    source: str
    count: int
    results: list[SamOpportunityResult]
