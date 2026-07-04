from datetime import date, datetime

from pydantic import BaseModel, Field


class OpportunityCreate(BaseModel):
    sam_notice_id: str | None = None
    title: str
    solicitation_number: str | None = None
    agency: str | None = None
    naics_code: str | None = None
    set_aside: str | None = None
    posted_date: date | None = None
    due_date: date | None = None
    status: str = "new"
    description: str | None = None


class OpportunityStatusUpdate(BaseModel):
    status: str


class OpportunityScoreUpdate(BaseModel):
    score: int = Field(..., ge=1, le=10)
    rationale: str | None = None


class OpportunityRead(BaseModel):
    id: int
    sam_notice_id: str | None = None
    title: str
    solicitation_number: str | None = None
    agency: str | None = None
    naics_code: str | None = None
    set_aside: str | None = None
    posted_date: date | None = None
    due_date: date | None = None
    status: str
    description: str | None = None
    qualification_score: int | None = None
    qualification_rationale: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
