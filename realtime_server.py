import flask
from flask import Flask, jsonify, send_from_directory
import pandas as pd
import random
import time
import threading
import datetime
import os

app = Flask(__name__, static_folder='web', static_url_path='')

# Global Data Store
data_lock = threading.Lock()
current_data = {
    'total_records': 12500000,
    'success_count': 110000, 
    'monthly_trends': {},
    'status_distribution': {'Success': 0, 'Rejected': 0, 'Pending': 0},
    'request_type_distribution': {'New Enrollment': 0, 'Biometric Update': 0, 'Demographic Update': 0},
    'state_enrollment': {},
    'anomalies': []
}

# Config
STATES = ['Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Bihar', 'West Bengal']
DISTRICTS = {
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra'],
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore'],
    'Delhi': ['New Delhi', 'North Delhi', 'South Delhi'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai'],
    'Bihar': ['Patna', 'Gaya', 'Muzaffarpur'],
    'West Bengal': ['Kolkata', 'Howrah', 'Darjeeling']
}

def init_mock_stats():
    """Initializes stats with some baseline data."""
    global current_data
    # Fill with some random initial values so charts aren't empty
    for s in STATES:
        current_data['state_enrollment'][s] = random.randint(10000, 50000)
    
    current_data['status_distribution'] = {
        'Success': int(current_data['total_records'] * 0.8),
        'Rejected': int(current_data['total_records'] * 0.15),
        'Pending': int(current_data['total_records'] * 0.05)
    }
    current_data['request_type_distribution'] = {
        'New Enrollment': int(current_data['total_records'] * 0.3),
        'Biometric Update': int(current_data['total_records'] * 0.4),
        'Demographic Update': int(current_data['total_records'] * 0.3)
    }
    
    # Generate last 12 months keys
    today = datetime.date.today()
    for i in range(11, -1, -1):
        m = (today - datetime.timedelta(days=30*i)).strftime('%Y-%m')
        current_data['monthly_trends'][m] = random.randint(5000, 15000)

import joblib
import numpy as np

# Load ML Model
print("Loading ML Model...")
try:
    model = joblib.load('src/model.pkl')
    encoders = joblib.load('src/encoders.pkl')
    print("ML Model Loaded Successfully.")
except:
    print("Warning: Model not found. Run src/ml_training.py first. Running in fallback mode.")
    model = None

def simulate_live_data():
    """Background thread to generate data every second."""
    global current_data
    while True:
        with data_lock:
            # Simulate a batch of new requests
            new_requests = random.randint(20, 100)
            current_data['total_records'] += new_requests
            
            # Distribute statuses
            success = int(new_requests * 0.85)
            rejected = int(new_requests * 0.1)
            pending = new_requests - success - rejected
            
            current_data['status_distribution']['Success'] += success
            current_data['status_distribution']['Rejected'] += rejected
            current_data['status_distribution']['Pending'] += pending
            
            # Update Current Month
            current_month = datetime.date.today().strftime('%Y-%m')
            if current_month not in current_data['monthly_trends']:
                current_data['monthly_trends'][current_month] = 0
            current_data['monthly_trends'][current_month] += new_requests
            
            # Update States & ML Inference
            for _ in range(new_requests):
                state = random.choice(STATES)
                district = random.choice(DISTRICTS[state])
                request_type_key = random.choice(['New Enrollment', 'Biometric Update', 'Demographic Update'])
                request_type = request_type_key # Keep for ML encoding
                
                # Update Request Stats
                if request_type_key not in current_data['request_type_distribution']:
                    current_data['request_type_distribution'][request_type_key] = 0
                current_data['request_type_distribution'][request_type_key] += 1
                gender = random.choice(['Male', 'Female', 'Transgender'])
                age = random.randint(1, 90)

                # Update State Counts
                if state not in current_data['state_enrollment']:
                    current_data['state_enrollment'][state] = 0
                current_data['state_enrollment'][state] += 1
                
                # ML Anomaly Check
                if model:
                    try:
                        # Encode features
                        # Handle unseen labels gracefully (fallback to 0 or arbitrary safe value)
                        e_state = encoders['State'].transform([state])[0] if state in encoders['State'].classes_ else 0
                        e_dist = encoders['District'].transform([district])[0] if district in encoders['District'].classes_ else 0
                        e_req = encoders['RequestType'].transform([request_type])[0] if request_type in encoders['RequestType'].classes_ else 0
                        e_gen = encoders['Gender'].transform([gender])[0] if gender in encoders['Gender'].classes_ else 0
                        
                        features = [[e_state, e_dist, e_req, e_gen, age]]
                        prediction = model.predict(features)[0] # 1 for normal, -1 for anomaly
                        
                        if prediction == -1:
                            # It's an Anomaly!
                            # Avoid duplicates
                            exists = any(a['District'] == district and a['State'] == state for a in current_data['anomalies'])
                            if not exists:
                                score = random.randint(85, 99) # Placeholder confidence score
                                current_data['anomalies'].insert(0, {
                                    'State': state,
                                    'District': district,
                                    'total': "LIVE DETECTED",
                                    'rejected': "ML ALERTS", 
                                    'rejection_rate': score # reusing this field for score
                                })
                                current_data['anomalies'] = current_data['anomalies'][:10]
                                
                    except Exception as e:
                        pass # Ignore encoding errors for now

        time.sleep(1) # Wait 1 second

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/api/stats')
def get_stats():
    with data_lock:
        response = {
            'summary': {
                'total_records': current_data['total_records'],
                'success_rate': round(current_data['status_distribution']['Success'] / current_data['total_records'] * 100, 2),
                'last_updated': datetime.datetime.now().strftime('%H:%M:%S')
            },
            'status_distribution': current_data['status_distribution'],
            'request_type_distribution': current_data['request_type_distribution'],
            'monthly_trends': current_data['monthly_trends'],
            'state_wise_enrollment': current_data['state_enrollment'],
            'anomalies': current_data['anomalies']
        }
    return jsonify(response)

if __name__ == '__main__':
    print("Starting Real-Time UIDAI Server...")
    print("Dashboard available at http://localhost:5000")
    
    init_mock_stats()
    
    # Start Simulation Thread
    sim_thread = threading.Thread(target=simulate_live_data, daemon=True)
    sim_thread.start()
    
    app.run(port=5000, debug=True, use_reloader=False) 
