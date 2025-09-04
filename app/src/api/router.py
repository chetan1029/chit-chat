from fastapi import APIRouter
from app.src.healthcheck.api import router as healthcheck_router
from app.src.messages.api import router as messages_router

router = APIRouter()

router.include_router(messages_router, prefix="/message", tags=["Message"])
router.include_router(healthcheck_router, prefix="", tags=["HealthCheck"])
