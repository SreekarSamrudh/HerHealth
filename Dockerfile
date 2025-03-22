FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh
WORKDIR /app
COPY requirements.txt .
COPY backend/main.py .
COPY data/fetus_health.py .
COPY data/risk_management.py .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["sh", "-c", "ollama serve & sleep 5 && ollama pull mistral && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
