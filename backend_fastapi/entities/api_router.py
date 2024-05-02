from fastapi import APIRouter

from entities.chat.router import router as chat_router

router = APIRouter()
router.include_router(chat_router, prefix="/rag_v1", tags=["chat"])
router.include_router(chat_router, prefix="/rag_v2", tags=["chat"])
