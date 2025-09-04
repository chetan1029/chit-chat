import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class Message(BaseModel):
    recipient: EmailStr
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(Message):
    @field_validator("content", mode="after")
    def validate_and_normalize_content(cls, v: str) -> str:
        normalized = v.strip()
        if not normalized:
            raise ValueError("Message content cannot be empty or just whitespace")
        return normalized


class MessageResponse(Message):
    id: uuid.UUID
    created_at: datetime


class MessageDeleteResponse(BaseModel):
    deleted_ids: List[uuid.UUID]
    not_found_ids: List[uuid.UUID] = []
