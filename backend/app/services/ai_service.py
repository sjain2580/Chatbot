import asyncio
import time
from typing import Dict, Any
from langchain_ollama import OllamaLLM
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, model: str = "llama2"):
        self.model = model
        self._initialize_llm()
    
    def _initialize_llm(self):
        try:
            self.llm = OllamaLLM(model=self.model, temperature=0.7)
            logger.info(f"Initialized Ollama with model {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    async def generate_response(self, message: str, history: list = None) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            context = self._build_context(history or [])
            full_prompt = f"{context}\nUser: {message}\nAssistant:"
            
            response = await asyncio.to_thread(self.llm.invoke, full_prompt)
            
            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)
            token_count = int(len(response.split()) * 1.3)
            
            return {
                "response": response,
                "response_time": response_time,
                "token_count": token_count,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def _build_context(self, history: list, max_messages: int = 5) -> str:
        if not history:
            return "You are a helpful AI assistant."
        
        recent_history = history[-max_messages:]
        context_parts = ["You are a helpful AI assistant. Previous conversation:"]
        
        for msg in recent_history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content", "")
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    async def health_check(self) -> bool:
        try:
            test_response = await asyncio.to_thread(self.llm.invoke, "Say 'OK'")
            return "OK" in test_response or "ok" in test_response.lower()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
