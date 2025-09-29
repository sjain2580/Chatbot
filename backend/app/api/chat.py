from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from ..services.ai_service import AIService
from ..core.database import get_db

router = APIRouter()
ai_service = AIService(model="llama2")

class ChatMessage(BaseModel):
    content: str
    conversation_id: Optional[str] = None

@router.post("/chat")
async def chat_message(message: ChatMessage, db: Session = Depends(get_db)):
    try:
        ai_response = await ai_service.generate_response(message.content)
        
        return {
            "id": "temp",
            "content": ai_response["response"],
            "role": "assistant",
            "timestamp": datetime.utcnow().isoformat(),
            "response_time": ai_response["response_time"],
            "token_count": ai_response["token_count"]
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.get("/health")
async def health_check():
    try:
        ai_healthy = await ai_service.health_check()
        return {
            "status": "healthy" if ai_healthy else "unhealthy",
            "ai_service": ai_healthy,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }
