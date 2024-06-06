from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from entities.api_router import router as api_router

app = FastAPI(title="forestinfo-bot")

# for production
app.add_middleware(
    CORSMiddleware,
    # for local dev
    # allow_origins=["*"],
    #for production
    allow_origins=["https://forestbot.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
