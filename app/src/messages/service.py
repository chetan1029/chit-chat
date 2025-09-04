import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.messages.datastore.implementation import MessageImplementation
from app.src.messages.models import (
    MessageCreate,
    MessageResponse,
    MessageDeleteResponse,
)


class MessagesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_message(self, message: MessageCreate) -> MessageResponse:
        message = await MessageImplementation(self.session).create_message(
            message=message
        )
        return message

    async def get_messages(self, recipient: str, limit: int) -> List[MessageResponse]:
        messages = await MessageImplementation(self.session).fetch_messages(
            recipient=recipient,
            limit=limit,
        )
        return messages

    async def remove_message(self, message_id: uuid.UUID) -> None:
        return await MessageImplementation(self.session).delete_message(
            message_id=message_id
        )

    async def remove_messages(
        self, message_ids: List[uuid.UUID]
    ) -> MessageDeleteResponse:
        return await MessageImplementation(self.session).delete_messages(
            message_ids=message_ids
        )
