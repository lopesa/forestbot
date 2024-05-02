from fastapi import FastAPI

from entities.api_router import router as api_router

app = FastAPI(title="forestinfo-bot")

app.include_router(api_router, prefix="/api")
