#!/bin/bash

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in the background (serving the Mistral model)
ollama serve &
ollama pull mistral  # Pull the Mistral model (used in your /chat endpoint)

# Start FastAPI and Streamlit
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
streamlit run frontend/app.py --server.port 8501
