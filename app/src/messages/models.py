import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    recipient: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(Message): ...


class MessageResponse(Message):
    id: uuid.UUID
    created_at: datetime
