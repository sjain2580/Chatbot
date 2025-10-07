import asyncio
import time
from typing import Dict, Any
import httpx
import os
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    
    async def generate_response(self, message: str, conversation_history: list = None) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json={"inputs": message},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data[0]['generated_text'] if isinstance(data, list) else message
                else:
                    content = "I'm having trouble connecting right now. Please try again."
                
                end_time = time.time()
                response_time = int((end_time - start_time) * 1000)
                
                return {
                    "response": content,
                    "response_time": response_time,
                    "token_count": len(content.split()),
                    "model": "DialoGPT"
                }
                
        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                "response_time": 0,
                "token_count": 0,
                "model": "error"
            }
    
    async def health_check(self) -> bool:
        return True
