from typing import AsyncGenerator, Any

from fastapi import FastAPI
from app.src.api.router import router
from contextlib import asynccontextmanager

from app.src.core.db import init_db


@asynccontextmanager
async def lifespan(
    _: FastAPI,
) -> AsyncGenerator[None, Any]:
    await init_db()
    yield


app = FastAPI(
    title="Chit Chat",
    description="Chit Chat endpoint services",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
