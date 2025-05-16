import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the CSV file relative to the script's directory
csv_path = os.path.join(script_dir, "data", "fetal_health.csv")

# Global variables
model = None
scaler = None
important_features = [
    'baseline value', 'accelerations', 'uterine_contractions',
    'prolongued_decelerations', 'mean_value_of_short_term_variability',
    'histogram_mean', 'histogram_variance'
]

def initialize_fetal_model():
    global model, scaler
    try:
        fetal_health_df = pd.read_csv(csv_path)
        fetal_health_df.drop_duplicates(inplace=True)
    except FileNotFoundError:
        print("Error: Fetal health dataset not found.")
        return False
    
    features = fetal_health_df[important_features]
    target = fetal_health_df['fetal_health']
    
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    return True

def predict_fetal_health(features):
    global model, scaler
    if model is None or scaler is None:
        raise ValueError("Fetal model not initialized. Call initialize_fetal_model() first.")
    input_data = np.array(features).reshape(1, -1)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    health_status = {1: "Normal", 2: "Suspect", 3: "Pathological"}
    return health_status.get(prediction, "Unknown")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_curve, auc    
    from sklearn.metrics import roc_curve, auc, f1_score, precision_recall_curve, classification_report
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.feature_selection import SelectFromModel
    from statistics import mean

    fetal_health_df = pd.read_csv(csv_path)
    fetal_health_df.drop_duplicates(inplace=True)

    print("Dataset Shape:", fetal_health_df.shape)
    print("\nFirst 5 rows:")
    print(fetal_health_df.head())
    print("\nDataset Information:")
    print(fetal_health_df.info())

    plt.figure(figsize=(12, 6))
    sns.countplot(x=fetal_health_df['fetal_health'], palette='viridis')
    plt.title('Fetal Health Distribution')
    plt.xlabel('Fetal Health (1: Normal, 2: Suspect, 3: Pathological)')
    plt.ylabel('Count')
    plt.show()

    plt.figure(figsize=(20, 12))
    correlation = fetal_health_df.corr()
    sns.heatmap(correlation, cmap="coolwarm", annot=True, annot_kws={"size": 8})
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.show()

    X = fetal_health_df.drop(columns=['fetal_health'])
    y = fetal_health_df['fetal_health']
    feature_selection_classifier = DecisionTreeClassifier()
    sfm = SelectFromModel(estimator=feature_selection_classifier)
    X_transformed = sfm.fit_transform(X, y)
    support = sfm.get_support()
    selected_cols = [col for col, selected in zip(X.columns, support) if selected]
    print(f"\nSelected features ({len(selected_cols)}):", selected_cols)

    initialize_fetal_model()
    print("\n=== Fetal Health Prediction System ===")
    print("Enter the following values:")
    feature_values = []
    for feature in important_features:
        while True:
            try:
                value = float(input(f"{feature}: "))
                feature_values.append(value)
                break
            except ValueError:
                print("Please enter a valid number.")
    
    prediction = predict_fetal_health(feature_values)
    print(f"\nPredicted Fetal Health: {prediction}")