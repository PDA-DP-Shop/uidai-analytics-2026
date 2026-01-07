# 🇮🇳 UIDAI Analytics Dashboard 2026
> **Unlocking Societal Trends in Aadhaar Enrolment & Updates**

## 🏆 Problem Statement addressed
**"Identify meaningful patterns, trends, anomalies, or predictive indicators and translate them into clear insights or solution frameworks that can support informed decision-making and system improvements."**

## 💡 Our Solution
This project is an **AI-Powered Real-Time Analytics Platform** that transforms raw Aadhaar transaction data into actionable intelligence.

### How we solved it:
| Problem Keyword | Our Feature Implementation |
|----------------|----------------------------|
| **"Meaningful Patterns"** | **Societal Trends Dashboard**: live visualization of the shift from *New Enrollments* to *Biometric/Demographic Updates*, indicating maturity in digital ID adoption. |
| **"Anomalies"** | **ML Engine (Isolation Forest)**: A trained Machine Learning model that scans every single transaction in real-time to flag statistical outliers (e.g., suspicious update clusters). |
| **"Predictive Indicators"** | **Confidence Scoring**: Each detected anomaly is assigned an ML Confidence Score to help officials prioritize investigations. |
| **"Informed Decision-Making"** | **Real-Time Control Center**: A centralized, glassmorphic dashboard that provides instant situational awareness to administrators. |

---

## 🚀 Key Features
- **⚡️ Real-Time Processing**: Ingests and visualizes enrollment data instantly (50+ transactions/second simulation).
- **🧠 AI Anomaly Detection**: Uses **Isolation Forest** (Unsupervised Learning) to detect fraud and operational issues.
- **📊 Interactive Visualizations**:
  - **Enrollment Trends**: Track growth over time.
  - **Societal Shifts**: Analyze the ratio of Enrollments vs Updates.
  - **Geographic Hotspots**: State-wise distribution.
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
   git clone https://github.com/PDA-DP-Shop/uidai-analytics-2026.git
   cd uidai-analytics-2026
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

## ⚖️ Disclaimer & Compliance
- **Synthetic Data Only**: This project uses purely **mock/synthetic data** generated programmatically. It does **not** access, store, or process any real Aadhaar data or PII (Personally Identifiable Information).
- **Educational Purpose**: This is a prototype designed for the **UIDAI 2026 Hackathon**. It is **not** an official government website or affiliated with UIDAI in any official capacity.
- **Fairness**: The Machine Learning models and algorithms are designed to detect statistical outliers without bias towards any gender, religion, or community.
