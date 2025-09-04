import uuid
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

from app.src.messages.datastore.dbmodel import Message as MessageTable
from app.src.messages.datastore.interface import MessageDataStore
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.messages.exceptions import DataStoreError, MessageNotFoundError
from app.src.messages.models import (
    MessageCreate,
    MessageResponse,
    MessageDeleteResponse,
)


class MessageImplementation(MessageDataStore):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_message(self, message: MessageCreate) -> MessageResponse:
        try:
            message_db = MessageTable(**message.model_dump())
            self.session.add(message_db)
            await self.session.commit()
            await self.session.refresh(message_db)

            return MessageResponse.model_validate(message_db)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DataStoreError("failed to create message") from e

    async def fetch_messages(self, recipient: str, limit: int) -> List[MessageResponse]:
        try:
            stmt = (
                select(MessageTable)
                .where(MessageTable.recipient == recipient)
                .order_by(MessageTable.created_at.asc())
                .limit(limit)
                .with_for_update(skip_locked=True)
            )
            result = await self.session.execute(stmt)
            messages = result.scalars().all()
            return [MessageResponse.model_validate(m) for m in messages]

        except SQLAlchemyError as e:
            raise DataStoreError("failed to fetch messages") from e

    async def delete_message(self, message_id: uuid.UUID) -> None:
        try:
            message = await self.session.get(MessageTable, message_id)
            if not message:
                raise MessageNotFoundError(
                    "Message not found with message id: {}".format(message_id)
                )

            await self.session.delete(message)
            await self.session.commit()

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DataStoreError("failed to delete message") from e

    async def delete_messages(
        self, message_ids: List[uuid.UUID]
    ) -> MessageDeleteResponse:
        try:
            stmt = select(MessageTable).where(MessageTable.id.in_(message_ids))
            result = await self.session.execute(stmt)
            messages = result.scalars().all()

            found_ids = [m.id for m in messages]
            not_found_ids = [mid for mid in message_ids if mid not in found_ids]

            if not messages:
                return MessageDeleteResponse(deleted_ids=[], not_found_ids=message_ids)

            for message in messages:
                await self.session.delete(message)

            await self.session.commit()

            return MessageDeleteResponse(
                deleted_ids=found_ids, not_found_ids=not_found_ids
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DataStoreError("failed to delete message") from e
