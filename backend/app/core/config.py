import os
from typing import List

class Settings:
    app_name: str = "AI Chatbot API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS origins
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://*.vercel.app",  # Your Vercel domain
        "*"  # Remove this in production for security
    ]
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
    
    # AI Settings
    ai_provider: str = os.getenv("AI_PROVIDER", "ollama")
    ai_model: str = os.getenv("AI_MODEL", "llama2")
    
    # Server
    port: int = int(os.getenv("PORT", "8000"))

settings = Settings()
