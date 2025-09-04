import uuid
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    recipient: str
    content: str

class MessageCreate(Message):
    ...

class MessageResponse(Message):
    id: uuid.UUID
    created_at: datetime