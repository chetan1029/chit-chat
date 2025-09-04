from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import text

from app.src.core.db import get_session

router = APIRouter()


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health_check_in():
    return {"status": "healthy"}


@router.get("/healthcheck/db", status_code=status.HTTP_200_OK)
async def health_check_db(session: get_session = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as _:
        raise HTTPException(status_code=503, detail="Database connection failed")
