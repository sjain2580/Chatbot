import asyncio
import time
from typing import Dict, Any
import httpx
import os
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - AI features will be limited")
    
    async def generate_response(
        self, 
        message: str, 
        conversation_history: list = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "response": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
                "response_time": 0,
                "token_count": 0,
                "model": "none"
            }
        
        start_time = time.time()
        
        try:
            # Build messages array with history
            messages = []
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content")
                    })
            
            messages.append({"role": "user", "content": message})
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"OpenAI API error: {response.text}")
                    raise Exception(f"API error: {response.status_code}")
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                end_time = time.time()
                response_time = int((end_time - start_time) * 1000)
                
                return {
                    "response": content,
                    "response_time": response_time,
                    "token_count": data.get("usage", {}).get("total_tokens", 0),
                    "model": "gpt-3.5-turbo"
                }
                
        except httpx.TimeoutException:
            logger.error("OpenAI API timeout")
            raise Exception("Request timeout - please try again")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
