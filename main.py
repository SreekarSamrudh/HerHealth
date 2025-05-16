from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import logging
import os
import requests
from twilio.rest import Client
import ollama
from dotenv import load_dotenv

from fetus_health import predict_fetal_health, initialize_fetal_model
from risk_management import predict_risk, initialize_risk_model  

# Load environment variables from .env file
logger = logging.getLogger(__name__)  # Move logger setup before load_dotenv
logging.basicConfig(level=logging.INFO)

logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Looking for .env file in: {os.path.abspath('.env')}")
if not os.path.exists(".env"):
    logger.error(".env file not found in the current directory!")
else:
    logger.info(".env file found, attempting to load...")

load_dotenv()

# Log the loaded environment variables
logger.info(f"TWILIO_ACCOUNT_SID after load_dotenv: {'Set' if os.getenv('TWILIO_ACCOUNT_SID') else 'Not set'}")
logger.info(f"TWILIO_AUTH_TOKEN after load_dotenv: {'Set' if os.getenv('TWILIO_AUTH_TOKEN') else 'Not set'}")
logger.info(f"TWILIO_PHONE_NUMBER after load_dotenv: {'Set' if os.getenv('TWILIO_PHONE_NUMBER') else 'Not set'}")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing models...")
    if not initialize_fetal_model():
        logger.error("Failed to initialize fetal health model.")
    else:
        logger.info("Fetal health model initialized.")
    initialize_risk_model()
    logger.info("Risk model initialized.")

class SOSRequest(BaseModel):
    latitude: float
    longitude: float
    emergency_contacts: List[str]

class ChatRequest(BaseModel):
    question: str

class HealthData(BaseModel):
    age: float
    systolic_bp: float
    diastolic_bp: float
    bs: float
    body_temp: float
    heart_rate: float

class FetalHealthData(BaseModel):
    baseline_value: float
    accelerations: float
    uterine_contractions: float
    prolongued_decelerations: float
    mean_value_of_short_term_variability: float
    histogram_mean: float
    histogram_variance: float

def validate_health_data(data: HealthData):
    if not (10 <= data.age <= 100): raise ValueError("Age must be between 10 and 100")
    if not (70 <= data.systolic_bp <= 200): raise ValueError("Systolic BP must be between 70 and 200")
    if not (40 <= data.diastolic_bp <= 120): raise ValueError("Diastolic BP must be between 40 and 120")
    if not (3.0 <= data.bs <= 20.0): raise ValueError("Blood Sugar must be between 3.0 and 20.0")
    if not (95.0 <= data.body_temp <= 105.0): raise ValueError("Body temperature must be between 95.0°F and 105.0°F")
    if not (40 <= data.heart_rate <= 180): raise ValueError("Heart rate must be between 40 and 180 bpm")

def validate_fetal_data(data: FetalHealthData):
    if not (100 <= data.baseline_value <= 200): raise ValueError("Baseline value must be between 100 and 200")
    if not (0 <= data.accelerations <= 1): raise ValueError("Accelerations must be between 0 and 1")
    if not (0 <= data.uterine_contractions <= 1): raise ValueError("Uterine contractions must be between 0 and 1")
    if not (0 <= data.prolongued_decelerations <= 1): raise ValueError("Prolongued decelerations must be between 0 and 1")

@app.post("/sos")
async def send_sos(request: SOSRequest):
    logger.info(f"Received SOS request: {request}")
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        logger.info(f"TWILIO_ACCOUNT_SID: {'Set' if account_sid else 'Not set'}")
        logger.info(f"TWILIO_AUTH_TOKEN: {'Set' if auth_token else 'Not set'}")
        logger.info(f"TWILIO_PHONE_NUMBER: {'Set' if from_number else 'Not set'}")

        if account_sid and auth_token and from_number:
            client = Client(account_sid, auth_token)
            sent_messages = []
            for contact in request.emergency_contacts:
                maps_link = f"https://www.google.com/maps?q={request.latitude},{request.longitude}"
                message_body = f"EMERGENCY ALERT: Help needed at Latitude: {request.latitude}, Longitude: {request.longitude}! View location: {maps_link}"
                try:
                    message = client.messages.create(body=message_body, from_=from_number, to=contact)
                    logger.info(f"Alert queued for {contact}, SID: {message.sid}")
                    import time
                    time.sleep(5)
                    updated_message = client.messages(message.sid).fetch()
                    status = updated_message.status
                    logger.info(f"Message status for {contact}: {status}")
                    sent_messages.append({"contact": contact, "sid": message.sid, "status": status})
                except Exception as e:
                    logger.error(f"Failed to send alert to {contact}: {str(e)}")
                    sent_messages.append({"contact": contact, "error": str(e)})
            all_delivered = all(msg.get("status") == "delivered" for msg in sent_messages if "status" in msg)
            return {
                "message": "SOS alert processed",
                "sent_messages": sent_messages,
                "simulated": False,
                "all_delivered": all_delivered
            }
        else:
            logger.info("Twilio credentials not found, simulating message")
            for contact in request.emergency_contacts:
                logger.info(f"Would send alert to {contact} - SIMULATION ONLY")
            return {"message": "SOS alert simulated (Twilio credentials missing)", "simulated": True, "all_delivered": False}
    except Exception as e:
        logger.error(f"Failed to process SOS request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send SOS alert: {str(e)}")

@app.post("/chat")
async def chat_with_janani(request: ChatRequest):
    try:
        formatted_question = f"As a maternal health assistant named Janani, please answer: {request.question}"
        try:
            response = ollama.chat(model="mistral", messages=[{"role": "user", "content": formatted_question}])
            return {"answer": response['message']['content']}
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return {"answer": f"Sorry, I couldn’t process your request: {str(e)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/predict_risk")
async def predict_risk_endpoint(data: HealthData):
    try:
        validate_health_data(data)
        risk_level, recommendations, _ = predict_risk(
            data.age, data.systolic_bp, data.diastolic_bp, data.bs, data.body_temp, data.heart_rate
        )
        return {"risk_level": risk_level, "recommendations": recommendations}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in risk prediction: {str(e)}")

@app.post("/predict_fetal_health")
async def predict_fetal_health_endpoint(data: FetalHealthData):
    try:
        validate_fetal_data(data)
        fetal_health_status = predict_fetal_health([
            data.baseline_value, data.accelerations, data.uterine_contractions,
            data.prolongued_decelerations, data.mean_value_of_short_term_variability,
            data.histogram_mean, data.histogram_variance
        ])
        return {"fetal_health": fetal_health_status}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in fetal health prediction: {str(e)}")

@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"message": "Server is alive!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000)) # Default to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)