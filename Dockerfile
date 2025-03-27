FROM python:3.11-slim

# Install curl and ollama
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt . 
COPY backend/main.py .
COPY fetus_health.py .
COPY risk_management.py .
COPY data/fetal_health.csv ./data/
COPY data/Maternal_Health_Risk_DataSet.csv ./data/
COPY frontend/app.py ./frontend/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the ollama mistral model
RUN ollama serve & sleep 5 && ollama pull mistral

# Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# CMD to run both FastAPI and Streamlit using supervisord
CMD ["sh", "-c", "ollama serve & uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]
