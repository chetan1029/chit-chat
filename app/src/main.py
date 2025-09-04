from fastapi import FastAPI
from app.src.api.router import router


app = FastAPI(
    title="Chit Chat",
    description="Chit Chat endpoint services",
    version="1.0.0",
)

app.include_router(router)
