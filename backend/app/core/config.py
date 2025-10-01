import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Scalable Chatbot API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    backend_cors_origins: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Allow all for now, restrict in production
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()
