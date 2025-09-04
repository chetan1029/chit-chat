from fastapi import APIRouter
from app.src.healthcheck.api import router as healthcheck_router

router = APIRouter()

router.include_router(healthcheck_router, prefix="", tags=["HealthCheck"])
