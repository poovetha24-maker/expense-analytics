import os
from dotenv import load_dotenv

import pandas as pd
import streamlit as st
import snowflake.connector
import plotly.express as px


# ==========================================
# Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="Expense Analytics",
    page_icon="💰",
    layout="wide"
)


# ==========================================
# Title
# ==========================================

st.title("💰 AI-Powered Personal Expense Analytics")
st.caption("Snowflake + Python ML + Streamlit")


# ==========================================
# Snowflake connection
# ==========================================

@st.cache_resource
def get_connection():

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="EXPENSE_ANALYTICS_DB",
        schema="ANALYTICS"
    )


conn = get_connection()


# ==========================================
# Helper function
# ==========================================

def run_query(query):

    cursor = conn.cursor()

    try:
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        return df

    finally:
        cursor.close()


# ==========================================
# Load data from Snowflake
# ==========================================

monthly = run_query("""
    SELECT *
    FROM EXPENSE_ANALYTICS_DB.ANALYTICS.MONTHLY_EXPENSES
    ORDER BY MONTH
""")


category = run_query("""
    SELECT *
    FROM EXPENSE_ANALYTICS_DB.ANALYTICS.CATEGORY_SUMMARY
    ORDER BY TOTAL_SPENDING DESC
""")


anomalies = run_query("""
    SELECT *
    FROM EXPENSE_ANALYTICS_DB.ML.ANOMALIES
    WHERE IS_ANOMALY = 'ANOMALY'
    ORDER BY AMOUNT DESC
""")


forecast = run_query("""
    SELECT *
    FROM EXPENSE_ANALYTICS_DB.ML.FORECASTS
    ORDER BY FORECAST_MONTH
""")


# ==========================================
# Prepare data
# ==========================================

monthly["MONTH"] = pd.to_datetime(monthly["MONTH"])

forecast["FORECAST_MONTH"] = pd.to_datetime(
    forecast["FORECAST_MONTH"]
)


# ==========================================
# KPI calculations
# ==========================================

total_spending = category["TOTAL_SPENDING"].sum()

total_transactions = category["TRANSACTION_COUNT"].sum()

average_transaction = (
    total_spending / total_transactions
)

anomaly_count = len(anomalies)


# ==========================================
# KPI Cards
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "💰 Total Spending",
        f"₹{total_spending:,.2f}"
    )


with col2:
    st.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )


with col3:
    st.metric(
        "📊 Avg Transaction",
        f"₹{average_transaction:,.2f}"
    )


with col4:
    st.metric(
        "🚨 Anomalies",
        anomaly_count
    )


# ==========================================
# Monthly Spending Trend
# ==========================================

st.subheader("📈 Monthly Spending Trend")


fig_monthly = px.line(
    monthly,
    x="MONTH",
    y="TOTAL_SPENDING",
    markers=True,
    title="Monthly Spending"
)


st.plotly_chart(
    fig_monthly,
    width="stretch"
)


# ==========================================
# Category Analysis
# ==========================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📊 Spending by Category")

    fig_category = px.bar(
        category,
        x="CATEGORY",
        y="TOTAL_SPENDING",
        title="Category-wise Spending"
    )

    st.plotly_chart(
        fig_category,
        width="stretch"
    )


with col2:

    st.subheader("🥧 Expense Distribution")

    fig_pie = px.pie(
        category,
        names="CATEGORY",
        values="TOTAL_SPENDING",
        title="Expense Distribution"
    )

    st.plotly_chart(
        fig_pie,
        width="stretch"
    )


# ==========================================
# Anomaly Detection
# ==========================================

st.subheader("🚨 Detected Anomalies")

st.write(
    f"Isolation Forest detected **{anomaly_count} unusual transactions**."
)


st.dataframe(
    anomalies,
    width="stretch"
)


# ==========================================
# Forecast
# ==========================================

st.subheader("🔮 Future Expense Forecast")


fig_forecast = px.line(
    forecast,
    x="FORECAST_MONTH",
    y="PREDICTED_AMOUNT",
    markers=True,
    title="Predicted Future Spending"
)


st.plotly_chart(
    fig_forecast,
    width="stretch"
)


# ==========================================
# Forecast Table
# ==========================================

st.subheader("📋 Forecast Details")


st.dataframe(
    forecast,
    width="stretch"
)




# ==========================================
# AI-Powered Financial Insights
# ==========================================

st.subheader("🤖 AI Financial Insights")

# ------------------------------------------
# 1. Highest spending category
# ------------------------------------------

highest_category = category.iloc[0]

category_insight = (
    f"Your highest spending category is "
    f"**{highest_category['CATEGORY']}**, "
    f"with total spending of "
    f"₹{highest_category['TOTAL_SPENDING']:,.2f}."
)

st.info("💰 " + category_insight)


# ------------------------------------------
# 2. Highest spending month
# ------------------------------------------

highest_month = monthly.loc[
    monthly["TOTAL_SPENDING"].idxmax()
]

lowest_month = monthly.loc[
    monthly["TOTAL_SPENDING"].idxmin()
]

month_insight = (
    f"Your highest monthly spending occurred in "
    f"**{highest_month['MONTH'].strftime('%B %Y')}**, "
    f"reaching ₹{highest_month['TOTAL_SPENDING']:,.2f}. "
    f"The lowest was in "
    f"**{lowest_month['MONTH'].strftime('%B %Y')}**, "
    f"at ₹{lowest_month['TOTAL_SPENDING']:,.2f}."
)

st.info("📊 " + month_insight)


# ------------------------------------------
# 3. Anomaly insight
# ------------------------------------------

if not anomalies.empty:

    largest_anomaly = anomalies.iloc[0]

    anomaly_insight = (
        f"The largest unusual transaction is "
        f"**{largest_anomaly['MERCHANT']}** for "
        f"₹{largest_anomaly['AMOUNT']:,.2f}. "
        f"This transaction was flagged by the "
        f"Isolation Forest model as an anomaly."
    )

    st.warning("🚨 " + anomaly_insight)


# ------------------------------------------
# 4. Forecast insight
# ------------------------------------------

if len(forecast) >= 2:

    first_prediction = forecast.iloc[0]["PREDICTED_AMOUNT"]
    last_prediction = forecast.iloc[-1]["PREDICTED_AMOUNT"]

    forecast_change = (
        (last_prediction - first_prediction)
        / first_prediction
    ) * 100

    if forecast_change > 0:

        forecast_insight = (
            f"Your predicted spending increases from "
            f"₹{first_prediction:,.2f} to "
            f"₹{last_prediction:,.2f}. "
            f"This represents an estimated increase of "
            f"**{forecast_change:.2f}%**."
        )

        st.warning("🔮 " + forecast_insight)

    else:

        forecast_insight = (
            f"Your predicted spending decreases by "
            f"approximately **{abs(forecast_change):.2f}%** "
            f"over the forecast period."
        )

        st.success("🔮 " + forecast_insight)


# ------------------------------------------
# 5. Overall recommendation
# ------------------------------------------

if anomaly_count >= 20:

    recommendation = (
        "A relatively high number of unusual transactions "
        "were detected. Review the anomaly table regularly "
        "to identify potentially incorrect or unexpected expenses."
    )

elif highest_category["TOTAL_SPENDING"] > total_spending * 0.30:

    recommendation = (
        f"Your spending is heavily concentrated in the "
        f"**{highest_category['CATEGORY']}** category. "
        f"Monitoring this category could help control "
        f"overall expenses."
    )

else:

    recommendation = (
        "Your spending is distributed across multiple "
        "categories. Continue monitoring monthly trends "
        "and unusual transactions."
    )

st.success("💡 **Recommendation:** " + recommendation)