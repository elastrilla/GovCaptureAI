from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProposalDraftRequest(BaseModel):
    company_id: int
    instructions: str | None = None


class ProposalDraftRead(BaseModel):
    id: int | None = None
    opportunity_id: int
    company_id: int
    title: str
    review_status: str = "draft_generated"
    readiness_score: int = 30
    review_notes: str | None = None
    executive_summary: str
    understanding: str
    technical_approach: str
    management_approach: str
    past_performance: str
    compliance_notes: list[str]
    review_gaps: list[str]
    draft_text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProposalReviewUpdate(BaseModel):
    review_status: str | None = None
    readiness_score: int | None = Field(default=None, ge=0, le=100)
    review_notes: str | None = None
    review_gaps: list[str] | None = None


class ProposalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    opportunity_id: int
    company_id: int
    title: str
    draft_text: str
    review_status: str
    readiness_score: int
    review_notes: str | None = None
    compliance_notes: list[str] = Field(default_factory=list)
    review_gaps: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
