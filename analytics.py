import pandas as pd
import json
import os

def run_analytics(input_file='data/aadhaar_mock_data.csv', output_file='web/dashboard_data.json'):
    """Reads Aadhaar data, performs analysis, and exports JSON for the dashboard."""
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run generate_mock_data.py first.")
        return

    df = pd.read_csv(input_file)
    
    # Analysis 1: Total Status Counts
    status_counts = df['Status'].value_counts().to_dict()
    
    # Analysis 2: Monthly Trends
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    monthly_trends = df.groupby('Month').size().to_dict()
    
    # Analysis 3: Rejection Reasons Distribution
    rejection_reasons = df[df['Status'] == 'Rejected']['RejectionReason'].value_counts().to_dict()
    
    # Analysis 4: State-wise Enrollment
    state_counts = df['State'].value_counts().to_dict()
    
    # Analysis 5: Anomaly Detection (Simple)
    # Flag districts with unusually high rejection rates (> 30%)
    district_stats = df.groupby(['State', 'District']).agg(
        total=('Status', 'count'),
        rejected=('Status', lambda x: (x == 'Rejected').sum())
    )
    district_stats['rejection_rate'] = (district_stats['rejected'] / district_stats['total']) * 100
    anomalies = district_stats[district_stats['rejection_rate'] > 25].reset_index()
    anomalies_list = anomalies.to_dict(orient='records')
    
    # Prepare Output
    output_data = {
        'summary': {
            'total_records': len(df),
            'success_rate': round((len(df[df['Status']=='Success']) / len(df)) * 100, 2),
            'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'status_distribution': status_counts,
        'monthly_trends': monthly_trends,
        'rejection_reasons': rejection_reasons,
        'state_wise_enrollment': state_counts,
        'anomalies': anomalies_list
    }
    
    # Ensure output directory exists (the web folder)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print(f"Analysis complete. Data exported to {output_file}")

if __name__ == "__main__":
    run_analytics()
