from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api import chat
from .core.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Chatbot API")
    create_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title="Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Chatbot API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)