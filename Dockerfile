FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh
WORKDIR /app
COPY requirements.txt .
COPY backend/main.py .
COPY backend/fetus_health.py .
COPY backend/risk_management.py .
COPY data/fetal_health.csv . 
COPY data/Maternal Health Risk Data Set.csv . 
RUN pip install --no-cache-dir -r requirements.txt
RUN ollama serve & sleep 5 && ollama pull mistral
EXPOSE 8000
CMD ["sh", "-c", "ollama serve & uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
