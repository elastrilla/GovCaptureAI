from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyProfileBase(BaseModel):
    website: str | None = None
    description: str | None = None
    core_capabilities: str | None = None
    differentiators: str | None = None
    certifications: str | None = None
    target_naics_codes: str | None = None
    target_agencies: str | None = None
    past_performance_summary: str | None = None


class CompanyCreate(CompanyProfileBase):
    name: str


class CompanyUpdate(CompanyProfileBase):
    name: str | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    website: str | None = None
    description: str | None = None
    core_capabilities: str | None = None
    differentiators: str | None = None
    certifications: str | None = None
    target_naics_codes: str | None = None
    target_agencies: str | None = None
    past_performance_summary: str | None = None
    created_at: datetime
