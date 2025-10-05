#!/bin/bash

echo "Starting Ollama service..."
ollama serve &
sleep 5

echo "Pulling llama2 model..."
ollama pull llama2

echo "Starting backend..."
cd backend
python3 -m app.main &
sleep 5

echo "Starting frontend..."
cd ../frontend
export REACT_APP_API_URL=http://localhost:8000/api/v1
npm install
npm start

wait
