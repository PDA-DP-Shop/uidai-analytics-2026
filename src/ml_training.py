import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import os
import numpy as np

# Config
DATA_PATH = 'data/aadhaar_mock_data.csv'
MODEL_PATH = 'src/model.pkl'
ENCODER_PATH = 'src/encoders.pkl'

def train_model():
    print("Loading data...")
    # Read only a subset for faster training demonstration (e.g., 100k rows)
    # Reading 10M rows might take too long for a quick demo
    df = pd.read_csv(DATA_PATH, nrows=100000) 
    
    print(f"Training on {len(df)} records...")

    # Features to use
    features = ['State', 'District', 'RequestType', 'Gender', 'Age']
    
    # Label Encoding (Convert text to numbers)
    encoders = {}
    for col in ['State', 'District', 'RequestType', 'Gender']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    # Prepare X
    X = df[features]
    
    # Train Isolation Forest
    # contamination=0.05 means we expect roughly 5% anomalies
    clf = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    clf.fit(X)
    
    # Save artifacts
    os.makedirs('src', exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(encoders, ENCODER_PATH)
    
    print("Model trained and saved to src/")

if __name__ == "__main__":
    train_model()
