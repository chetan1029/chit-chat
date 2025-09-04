import uuid
import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.src.messages.datastore.implementation import MessageImplementation
from app.src.messages.models import (
    MessageCreate,
    MessageResponse,
    MessageDeleteResponse,
)

logger = logging.getLogger(__name__)


class MessagesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_message(self, message: MessageCreate) -> MessageResponse:
        message = await MessageImplementation(self.session).create_message(
            message=message
        )

        logger.info(
            "Setting Message",
            extra={
                "extra_info": {
                    "message": message.model_dump_json(),
                }
            },
        )
        return message

    async def get_new_messages(
        self, recipient: str, limit: int
    ) -> List[MessageResponse]:
        messages = await MessageImplementation(self.session).fetch_new_messages(
            recipient=recipient,
            limit=limit,
        )
        logger.info(
            "Getting new Messages",
            extra={
                "extra_info": {
                    "messages": messages,
                }
            },
        )
        return messages

    async def get_messages(
        self, recipient: str, start: int, stop: int, order: str
    ) -> List[MessageResponse]:
        messages = await MessageImplementation(self.session).fetch_messages(
            recipient=recipient,
            start=start,
            stop=stop,
            order=order,
        )
        logger.info(
            "Getting all Messages",
            extra={
                "extra_info": {
                    "messages": messages,
                }
            },
        )
        return messages

    async def remove_message(self, message_id: uuid.UUID) -> None:
        logger.info(
            "Removing Single Message",
            extra={
                "extra_info": {
                    "message_id": str(message_id),
                }
            },
        )
        return await MessageImplementation(self.session).delete_message(
            message_id=message_id
        )

    async def remove_messages(
        self, message_ids: List[uuid.UUID]
    ) -> MessageDeleteResponse:
        logger.info(
            "Removing Multiple Messages",
            extra={
                "extra_info": {
                    "message_ids": [str(mid) for mid in message_ids],
                }
            },
        )
        return await MessageImplementation(self.session).delete_messages(
            message_ids=message_ids
        )
