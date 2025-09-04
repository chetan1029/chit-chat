from fastapi import APIRouter, status

router = APIRouter()


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health_check_in():
    return {"status": "healthy"}
