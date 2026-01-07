import pandas as pd
import random
import datetime
import os

from src.india_data import INDIA_DATA

def generate_mock_data(num_records=1000000):
    """Generates synthetic Aadhaar enrollment and update data."""
    
    states = list(INDIA_DATA.keys())
    
    # We will pick districts based on the chosen state
    
    request_types = ['New Enrollment', 'Biometric Update', 'Demographic Update', 'Mobile Update']
    genders = ['Male', 'Female', 'Transgender']
    statuses = ['Success', 'Rejected', 'Pending']
    rejection_reasons = ['Duplicate', 'Document Mismatch', 'Biometric Low Quality', 'Technical Error', '']

    data = []
    
    start_date = datetime.date(2001, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    
    for _ in range(num_records):        
        state = random.choice(states)
        district = random.choice(INDIA_DATA[state])
        
        request_type = random.choice(['New Enrollment', 'Biometric Update', 'Demographic Update', 'Mobile Update'])
        gender = random.choice(genders) # This line was not in the provided snippet, but was in the original code and should be kept.
        age = random.randint(1, 90)
        
        # Simulate some logic: New enrollments mostly successful, updates vary
        status = random.choices(statuses, weights=[70, 20, 10], k=1)[0]
        
        reason = ''
        if status == 'Rejected':
            reason = random.choice(rejection_reasons[:-1]) # Pick a reason
            
        date_occured = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        
        data.append({
            'State': state,
            'District': district,
            'RequestType': request_type,
            'Gender': gender,
            'Age': age,
            'Date': date_occured,
            'Status': status,
            'RejectionReason': reason
        })
        
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs('data', exist_ok=True)
    
    output_path = 'data/aadhaar_mock_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {num_records} records to {output_path}")

if __name__ == "__main__":
    generate_mock_data(10000000)
