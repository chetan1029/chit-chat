from fastapi import FastAPI
from app.src.api.router import router


app = FastAPI(
    title="Astro Ai Agent",
    description="Astro Ai Agent Api endpoint services",
    version="1.0.0",
)

app.include_router(router)
