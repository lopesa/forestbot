from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

from entities.api_router import router as api_router

app = FastAPI(title="forestinfo-bot")

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# for production
# for local dev
#for production
# allow_origins=["https://forestbot.vercel.app/"],