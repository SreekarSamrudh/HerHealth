
# HerHealth: Maternal and Fetal Health Monitoring Application

HerHealth is a comprehensive web application designed to support maternal and fetal well-being. It offers features for health risk prediction, fetal health status monitoring, an AI-powered chatbot for maternal health queries, SOS emergency alerts, and weather updates.

The application consists of a Streamlit frontend for user interaction and a FastAPI backend to handle predictions, API integrations, and other logic.

---

## ✅ Features

- **Health Risk Predictor**: Assesses maternal health risk based on vital signs such as age, blood pressure, blood sugar, body temperature, and heart rate.
- **Fetal Health Prediction**: Predicts fetal health status (Normal, Suspect, Pathological) based on cardiotocography parameters.
- **Janani Bot**: An AI chatbot to answer maternal health-related questions. This can be configured to use a local Ollama instance or an external LLM API (like Hugging Face Inference API).
- **SOS Emergency Alerts**: Allows users to send their current location (automatically detected or manually entered) to pre-defined emergency contacts via SMS (powered by Twilio).
- **Weather Updates**: Provides current weather information for a specified city using the OpenWeatherMap API.
- **User-Friendly Interface**: Built with Streamlit, featuring a custom navigation bar and interactive elements for data input and results display.

---

## 🗂️ Project Structure

```
HerHealth/
├── app.py                # Streamlit frontend application
├── main.py               # FastAPI backend application
├── fetus_health.py       # Logic and model for fetal health prediction
├── risk_management.py    # Logic and model for maternal health risk prediction
├── requirements.txt      # Python dependencies for the entire project
├── .env.example          # Example template for environment variables
├── .gitignore            # Specifies intentionally untracked files that Git should ignore
├── assets/               # Static assets for the frontend (images, icons)
│   ├── gynae_genius.png
│   ├── maternal-bg.jpg
│   └── hero-bg.jpg
└── data/                 # CSV data files for training/initializing the models
    ├── fetal_health.csv
    └── Maternal_Health_Risk_Data_Set.csv
```

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn (ASGI server), Gunicorn (WSGI HTTP server for production)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **APIs & Services**:
  - Twilio API (for SOS SMS alerts)
  - OpenWeatherMap API (for weather updates)
  - Ollama / Hugging Face Inference API (for Janani Bot)
  - Geocoder & Geopy (for location services)
- **Styling**: Custom CSS injected into Streamlit
- **Environment Management**: `python-dotenv`

---

## 💻 Local Installation Guide

### 🧾 Prerequisites

- Python 3.8+
- pip
- Git
- (Recommended) `venv` or `conda`
- (Optional) Ollama app with a downloaded model (`ollama pull mistral`)

---

### 🚀 Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/SreekarSamrudh/HerHealth.git
cd HerHealth
```

#### 2. Create and Activate a Virtual Environment

##### Using venv:

```bash
python -m venv wealenv
# Windows:
wealenv\Scripts\activate
# macOS/Linux:
source wealenv/bin/activate
```

##### Or using conda:

```bash
conda create -n herhealth_env python=3.9
conda activate herhealth_env
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file using the `.env.example` template.

```ini
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_twilio_auth_token_here"
TWILIO_PHONE_NUMBER="+1yourTwilioPhoneNumberHere"
OPENWEATHER_API_KEY="your_openweathermap_api_key_here"
HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# BACKEND_API_URL="http://127.0.0.1:8000"
# OLLAMA_HOST="http://localhost:11434"
```

#### 5. Ensure Correct Paths

- Data files must be in the `data/` directory
- Image assets must be in the `assets/` directory
- Use `os.path.join()` for portability in your Python code

---

## 🧪 Running the Application

### A. Start the FastAPI Backend

```bash
python main.py
```

### B. Start the Streamlit Frontend

In a **new terminal**, run:

```bash
streamlit run app.py
```

---

## 📲 Using the Application

- **Health & Fetal Predictions**: Input the required medical details and view predictions.
- **Janani Bot**:
  - With **Ollama**: Ensure the Ollama app is running with a model pulled (`ollama pull mistral`)
  - With **Hugging Face**: Ensure `HF_TOKEN` is configured
- **SOS Alerts**: Send test SMS using a verified Twilio number
- **Weather**: Enter your city and get real-time weather info

---

## 🧯 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure the virtual environment is activated and dependencies are installed |
| `FileNotFoundError` | Check if all required files exist in `data/` and `assets/` |
| API Not Responding | Confirm FastAPI backend is running and correct URLs are set |
| Ollama Not Working | Ensure Ollama is installed, running, and model is available |
| Twilio SMS Not Sent | Ensure Twilio credentials are valid and your phone number is verified |

---


## 🙌 Acknowledgments

- [Twilio](https://www.twilio.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [Ollama](https://ollama.com/)
- [Hugging Face](https://huggingface.co/)
