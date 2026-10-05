import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector
from sklearn.linear_model import LinearRegression

load_dotenv()

# --------------------------------
# 1. Connect to Snowflake
# --------------------------------

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database="EXPENSE_ANALYTICS_DB",
    schema="ANALYTICS"
)

print("Connected to Snowflake successfully!")


# --------------------------------
# 2. Get monthly spending
# --------------------------------

query = """
SELECT
    MONTH,
    TOTAL_SPENDING
FROM EXPENSE_ANALYTICS_DB.ANALYTICS.MONTHLY_EXPENSES
ORDER BY MONTH
"""

df = pd.read_sql(query, conn)

print("Monthly records:", len(df))

print("\nHistorical spending:")
print(df)


# --------------------------------
# 3. Prepare data for ML
# --------------------------------

df["MONTH"] = pd.to_datetime(df["MONTH"])

df["MONTH_NUMBER"] = range(1, len(df) + 1)

X = df[["MONTH_NUMBER"]]
y = df["TOTAL_SPENDING"]


# --------------------------------
# 4. Train Linear Regression
# --------------------------------

model = LinearRegression()

model.fit(X, y)


# --------------------------------
# 5. Predict next 3 months
# --------------------------------

future_numbers = [[
    len(df) + 1
], [
    len(df) + 2
], [
    len(df) + 3
]]

predictions = model.predict(future_numbers)


# --------------------------------
# 6. Create forecast dataframe
# --------------------------------

last_month = df["MONTH"].max()

future_months = pd.date_range(
    start=last_month + pd.DateOffset(months=1),
    periods=3,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "FORECAST_MONTH": future_months,
    "PREDICTED_AMOUNT": predictions
})

forecast_df["FORECAST_MONTH"] = forecast_df["FORECAST_MONTH"].dt.date

forecast_df["PREDICTED_AMOUNT"] = (
    forecast_df["PREDICTED_AMOUNT"]
    .clip(lower=0)
    .round(2)
)

print("\nFuture forecast:")
print(forecast_df)


# --------------------------------
# 7. Save to Snowflake
# --------------------------------

cursor = conn.cursor()

cursor.execute("""
TRUNCATE TABLE EXPENSE_ANALYTICS_DB.ML.FORECASTS
""")

records = list(
    forecast_df.itertuples(
        index=False,
        name=None
    )
)

insert_query = """
INSERT INTO EXPENSE_ANALYTICS_DB.ML.FORECASTS
(
    FORECAST_MONTH,
    PREDICTED_AMOUNT
)
VALUES (%s, %s)
"""

cursor.executemany(
    insert_query,
    records
)

print("\nForecast saved to Snowflake!")


# --------------------------------
# 8. Close connection
# --------------------------------

cursor.close()
conn.close()

print("Forecasting completed successfully!")