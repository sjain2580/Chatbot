#!/usr/bin/env bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Pull the llama2 model
ollama pull llama2 || echo "Ollama model pull failed, will retry at runtime"
