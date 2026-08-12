from pydantic import BaseModel, Field


class SamSearchRequest(BaseModel):
    keyword: str | None = None
    naics_code: str | None = None
    agency: str | None = None
    set_aside: str | None = None
    notice_type: str | None = None
    posted_from: str | None = Field(
        default=None,
        description="Start posted date in MM/DD/YYYY format"
    )
    posted_to: str | None = Field(
        default=None,
        description="End posted date in MM/DD/YYYY format"
    )
    limit: int = Field(default=10, ge=1, le=100)


class SamOpportunityResult(BaseModel):
    sam_notice_id: str
    title: str
    solicitation_number: str | None = None
    notice_type: str | None = None
    agency: str | None = None
    naics_code: str | None = None
    set_aside: str | None = None
    posted_date: str | None = None
    due_date: str | None = None
    summary: str | None = None
    description: str | None = None


class SamSearchResponse(BaseModel):
    source: str
    count: int
    results: list[SamOpportunityResult]
