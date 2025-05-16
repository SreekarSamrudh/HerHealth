import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the CSV file relative to the script's directory
csv_path = os.path.join(script_dir, "data", "Maternal_Health_Risk_Data_Set.csv")
df = pd.read_csv(csv_path)

# Global variables
scaler = None
best_rf = None
label_encoder = None

def initialize_risk_model():
    global scaler, best_rf, label_encoder
    df = pd.read_csv(csv_path)
    
    label_encoder = LabelEncoder()
    df['RiskLevel'] = label_encoder.fit_transform(df['RiskLevel'])
    
    selected_features = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']
    X = df[selected_features]
    y = df['RiskLevel']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20, 30], 'min_samples_split': [2, 5, 10]}
    grid_search = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    global best_rf
    best_rf = grid_search.best_estimator_

def predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    global scaler, best_rf, label_encoder
    if best_rf is None or scaler is None or label_encoder is None:
        raise ValueError("Risk model not initialized. Call initialize_risk_model() first.")
    sample = np.array([[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]])
    sample_scaled = scaler.transform(sample)
    prediction = best_rf.predict(sample_scaled)[0]
    risk_label = label_encoder.inverse_transform([prediction])[0]
    
    if risk_label == 'high risk':
        message = "You are at high risk! Please meet your doctor immediately for a checkup."
    elif risk_label == 'mid risk':
        message = "You are at moderate risk. It's advised to consult your doctor soon."
    else:
        message = "You are at low risk. Maintain a healthy lifestyle and monitor regularly."
    
    return risk_label, message, sample

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    
    initialize_risk_model()
    df = pd.read_csv(csv_path)
    df['RiskLevel'] = label_encoder.fit_transform(df['RiskLevel'])
    X = df[['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']]
    y = df['RiskLevel']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_test_scaled = scaler.transform(X_test)
    y_pred = best_rf.predict(X_test_scaled)
    
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    
    print("Enter the following health details:")
    age = float(input("Age: "))
    systolic_bp = float(input("SystolicBP: "))
    diastolic_bp = float(input("DiastolicBP: "))
    bs = float(input("Blood Sugar (mmol/L): "))
    body_temp = float(input("BodyTemp (°F): "))
    heart_rate = float(input("HeartRate (bpm): "))
    
    predicted_risk, risk_message, user_sample = predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate)
    print(f"Predicted Risk Level: {predicted_risk}")
    print(risk_message)
    
    plt.figure(figsize=(10, 6))
    plt.bar(['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate'], user_sample[0], color='blue', alpha=0.6)
    plt.axhline(y=80, color='red', linestyle='--', label='High Risk Threshold')
    plt.axhline(y=60, color='orange', linestyle='--', label='Mid Risk Threshold')
    plt.xlabel("Health Parameters")
    plt.ylabel("Values")
    plt.title("User Health Parameters with Risk Baseline")
    plt.legend()
    plt.show()