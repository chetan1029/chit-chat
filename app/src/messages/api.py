import uuid
from typing import List

from fastapi import APIRouter, status, Query, Depends, HTTPException

from app.src.messages.exceptions import DataStoreError, MessageNotFoundError
from app.src.messages.models import MessageCreate, MessageResponse
from app.src.messages.service import MessagesService
from app.src.core.db import get_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def set_message(
    message: MessageCreate, session: get_session = Depends(get_session)
) -> MessageResponse:
    try:
        return await MessagesService(session).set_message(message)
    except DataStoreError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/new", status_code=status.HTTP_200_OK, response_model=List[MessageResponse]
)
async def get_new_messages(
    recipient: str = Query(...),
    limit: int = Query(100, gt=0),
    session: get_session = Depends(get_session),
) -> List[MessageResponse]:
    try:
        return await MessagesService(session).get_messages(recipient, limit)
    except DataStoreError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[MessageResponse])
async def get_messages(
    recipient: str = Query(...),
    start: int = Query(0, ge=0),
    stop: int = Query(50, gt=0),
    order: str = Query("asc", regex="^(asc|desc)$"),
) -> List[MessageResponse]: ...


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_message(
    message_id: uuid.UUID, session: get_session = Depends(get_session)
) -> None:
    try:
        return await MessagesService(session).remove_message(message_id=message_id)
    except MessageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DataStoreError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/delete", status_code=status.HTTP_200_OK)
async def remove_messages(message_ids: List[uuid.UUID]) -> None: ...
