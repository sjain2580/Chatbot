#!/usr/bin/env bash
# Start Ollama in the background
ollama serve &

# Wait for Ollama to be ready
sleep 5

# Pull model if not already downloaded
ollama pull llama2

# Start FastAPI application
cd backend && python -m app.main
