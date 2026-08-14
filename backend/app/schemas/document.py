from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


DocumentType = Literal[
    "capability_statement",
    "certification",
    "past_performance",
    "key_personnel",
    "other",
]


class DocumentCreate(BaseModel):
    document_type: DocumentType
    title: str
    filename: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    file_data: str | None = None
    content_text: str | None = None
    notes: str | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    document_type: DocumentType
    title: str
    filename: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    content_text: str | None = None
    notes: str | None = None
    created_at: datetime
