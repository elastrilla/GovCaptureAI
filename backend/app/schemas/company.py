from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None
    description: str | None = None


class CompanyRead(BaseModel):
    id: int
    name: str
    website: str | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
