from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from typing import AsyncGenerator

from sqlmodel import SQLModel
from app.src.core.config import get_settings

_engine = None
_async_session_maker = None


def get_session_maker():
    global _async_session_maker
    if _async_session_maker is None:
        _async_session_maker = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _async_session_maker


def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url, echo=settings.app_env == "development", future=True
        )
    return _engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = get_session_maker()
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    async with get_engine().begin() as conn:
        # TODO: add datamodel in the next setup
        await conn.run_sync(SQLModel.metadata.create_all)
