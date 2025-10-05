from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from .api import chat
from .core.database import create_tables

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify key is loaded
if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key loaded successfully")
else:
    print("WARNING: OpenAI API key not found!")
    
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Chatbot API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
