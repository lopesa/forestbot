from fastapi import APIRouter

from entities.chat.router import router as chat_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["chat"])
