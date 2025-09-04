import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    recipient: str = Field(index=True, nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    fetched_at: datetime = Field(default=None, nullable=True, index=True)
