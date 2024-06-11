from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from entities.api_router import router as api_router

app = FastAPI(title="forestinfo-bot")

# uncomment for dev
# production cors is in the
# Digital Ocean app settings on their wysiwyg
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["X-docs"]
# )

app.include_router(api_router, prefix="/api")
