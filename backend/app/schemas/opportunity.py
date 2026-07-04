from datetime import date, datetime

from pydantic import BaseModel


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
    created_at: datetime

    class Config:
        from_attributes = True
