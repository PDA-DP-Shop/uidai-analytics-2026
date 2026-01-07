# 🇮🇳 UIDAI Analytics Dashboard 2026
> **A Real-Time, AI-Powered Anomaly Detection Platform for Aadhaar Data**

## 🏆 Project Overview
This project was built for the **UIDAI Data Hackathon 2026**. It is a next-generation analytics dashboard designed to monitor Aadhaar enrollment trends in real-time and detect fraudulent or anomalous patterns using Machine Learning.

### 🌟 Key Features
- **⚡️ Real-Time Processing**: Ingests and visualizes enrollment data instantly (50+ transactions/second simulation).
- **🧠 AI Anomaly Detection**: Uses an **Isolation Forest** Machine Learning model to flag suspicious demographic/biometric update patterns.
- **📊 Interactive Dashboard**: A premium, glassmorphism-styled UI with live chart updates.
- **🚨 Instant Alerts**: Priority alert system for districts with high rejection rates or ML-flagged anomalies.

## 🛠 Tech Stack
- **Backend**: Python, Flask (Streaming API)
- **Machine Learning**: Scikit-Learn (Isolation Forest), Pandas, NumPy
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js
- **Data**: Synthetic Data Generator (Simulates 10M+ records)

## 🚀 How to Run
### Prerequisites
- Python 3.8+
- Pip

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd aadhaar-website
   ```
2. Install dependencies:
   ```bash
   pip install flask pandas scikit-learn joblib
   ```

### Running the System
1. **(Optional) Retrain ML Model**:
   If you want to regenerate the anomaly detection model:
   ```bash
   python3 src/ml_training.py
   ```
2. **Start the Real-Time Server**:
   ```bash
   python3 realtime_server.py
   ```
3. **Access Dashboard**:
   Open **[http://localhost:5000](http://localhost:5000)** in your browser.

## 🧪 Simulation Details
The `simulate_live_data` engine generates realistic variations in:
- **Request Types**: Biometric, Demographic, Mobile Updates.
- **Outcomes**: Success, Rejected, Pending.
- **Anomalies**: Random injection of statistical outliers to test the ML engine.

## 🔮 Future Scope
- Integration with live UIDAI API (secure sandbox).
- GIS Mapping for geospatial visualization of enrollment centers.
- LLM-powered natural language reporting (e.g., *"Summarize today's trends"*).

---
*Built with ❤️ for Digital India.*
