# Use a lightweight Python base image
FROM python:3.11-slim

# Install system dependencies (curl for Ollama)
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory inside the container
WORKDIR /app

COPY requirements.txt .
COPY backend/main.py .
COPY fetus_health.py .
COPY risk_management.py .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pull the Mistral model during build
RUN ollama pull mistral

# Expose the port Render will use (default 8000, overridden by $PORT)
EXPOSE 8000

# Start Ollama and FastAPI when the container runs
CMD ["sh", "-c", "ollama serve & uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
