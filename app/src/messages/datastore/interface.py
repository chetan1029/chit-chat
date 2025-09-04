import uuid
from typing import Protocol, List

from app.src.messages.models import MessageCreate, MessageResponse


class MessageDataStore(Protocol):
    async def create_message(self, message: MessageCreate) -> MessageResponse: ...
    async def fetch_messages(
        self, recipient: str, limit: int
    ) -> List[MessageResponse]: ...
    async def delete_message(self, message_id: uuid.UUID) -> None: ...
