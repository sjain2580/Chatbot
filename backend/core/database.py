# backend/core/database.py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///chatbot.db")
__all__ = ["engine"]  # Optional, for explicit exports