# 💰 AI-Powered Personal Expense & Financial Analytics

An end-to-end financial analytics project that uses **Snowflake as the central data warehouse** and **Python Machine Learning** to analyze personal transaction data, detect unusual spending patterns, forecast future expenses, and present insights through an interactive Streamlit dashboard.

---

## 🚀 Project Overview

Managing personal expenses manually can make it difficult to identify spending patterns, unusual transactions, and future financial trends.

This project provides a data-driven solution by combining:

- Snowflake for cloud data storage and analytics
- Python for data processing
- Machine Learning for anomaly detection and forecasting
- Streamlit for interactive visualization
- Automated insights for easier financial interpretation

The system processes transaction data and transforms it into actionable financial insights.

---

## 🎯 Objectives

- Analyze personal spending behavior
- Identify monthly and category-wise spending patterns
- Detect unusual or potentially suspicious transactions
- Predict future monthly expenses
- Provide automated financial insights
- Demonstrate an end-to-end Snowflake + ML analytics workflow

---

## 🏗️ System Architecture

```text
                  Transaction Dataset
                         │
                         ▼
                  Python Data Generator
                         │
                         ▼
                 ┌─────────────────┐
                 │    Snowflake    │
                 │                 │
                 │  RAW Schema     │
                 │  Transactions   │
                 └────────┬────────┘
                          │
                          ▼
                 Analytics Processing
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       Monthly Analysis        Category Analysis
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                   Python ML Models
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      Isolation Forest          Linear Regression
      Anomaly Detection             Forecasting
             │                         │
             ▼                         ▼
       ML.ANOMALIES             ML.FORECASTS
             │                         │
             └────────────┬────────────┘
                          ▼
                  Streamlit Dashboard
                          │
                          ▼
                 Financial Insights




📊 Dataset
The project uses a generated transaction dataset containing 2,005 transactions.
Dataset Columns
Column	Description
transaction_id	Unique transaction identifier
transaction_date	Date of transaction
category	Expense category
merchant	Merchant or service
amount	Transaction amount
payment_method	Payment method
description	Transaction description


❄️ Snowflake Structure
Database
EXPENSE_ANALYTICS_DB

Schemas
RAW
ANALYTICS
ML
PUBLIC

Raw Data
RAW.TRANSACTIONS

The raw transaction dataset contains 2,005 records.
Machine Learning Results
ML.ANOMALIES
ML.FORECASTS

🚨 Anomaly Detection
The project uses the Isolation Forest algorithm from Scikit-learn.
The model analyzes transaction amounts and spending patterns to identify transactions that significantly differ from normal behavior.
Result
Transactions analyzed: 2,005
Anomalies detected: 21

Example high-value anomaly:
Merchant: Amazon
Category: Shopping
Amount: ₹75,000
Payment Method: Card

The detected anomalies are stored in:
EXPENSE_ANALYTICS_DB.ML.ANOMALIES

🔮 Expense Forecasting
A Linear Regression model is used as a baseline forecasting model.
Historical monthly spending is used to predict future expenses.
Forecast
Month	Predicted Spending
January 2027	₹548,932.21
February 2027	₹559,880.83
March 2027	₹570,829.45


The predictions are stored in:
EXPENSE_ANALYTICS_DB.ML.FORECASTS

📈 Dashboard
The Streamlit dashboard provides:
Key Metrics
- Total spending
- Number of transactions
- Average transaction amount
- Number of detected anomalies
Visualizations
- Monthly spending trend
- Category-wise spending
- Expense distribution
- Anomaly transactions
- Future expense forecast
Financial Insights
The dashboard automatically generates insights about:
- Highest spending category
- Highest and lowest spending months
- Unusual transactions
- Forecasted spending trends
- General spending recommendations
📁 Project Structure
expense-analytics/
│
├── app.py
├── generate_data.py
├── anomaly_detection.py
├── forecasting.py
├── transactions.csv
├── requirements.txt
├── .gitignore
├── README.md
└── .env

.env contains credentials and must not be committed to GitHub.

⚙️ Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd expense-analytics

2. Install dependencies
pip install -r requirements.txt

3. Configure Snowflake credentials
Create a .env file:
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH

Do not share or commit this file.
▶️ Running the Project
Generate transaction data
python generate_data.py

Run anomaly detection
python anomaly_detection.py

Run expense forecasting
python forecasting.py

Launch the dashboard
python -m streamlit run app.py

The dashboard will be available at:
http://localhost:8501

🔐 Security
Sensitive Snowflake credentials are stored using environment variables.
The .env file is excluded from Git using .gitignore.
Example:
.env
__pycache__/
*.pyc

📌 Key Results
Metric	Result
Transactions processed	2,005
Anomalies detected	21
Forecast horizon	3 months
Data warehouse	Snowflake
ML algorithm	Isolation Forest
Forecasting model	Linear Regression
Dashboard	Streamlit


🔮 Future Enhancements
- Advanced time-series forecasting using models such as ARIMA or Prophet
- More sophisticated anomaly detection
- Personalized budget recommendations
- Real-time transaction ingestion
- LLM-based financial explanations
- User authentication
- Expense alerts
- Interactive budget planning
- Deployment to Streamlit Cloud
👨‍💻 Project
AI-Powered Personal Expense & Financial Analytics
Built using:
Snowflake + Python + Machine Learning + Streamlit