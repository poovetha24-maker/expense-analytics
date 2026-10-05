import os
from dotenv import load_dotenv
import pandas as pd
import snowflake.connector
from sklearn.ensemble import IsolationForest

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
    schema="RAW"
)

print("Connected to Snowflake successfully!")


# --------------------------------
# 2. Read transactions
# --------------------------------

query = """
SELECT
    TRANSACTION_ID,
    TRANSACTION_DATE,
    CATEGORY,
    MERCHANT,
    AMOUNT,
    PAYMENT_METHOD
FROM TRANSACTIONS
"""

df = pd.read_sql(query, conn)

print("Transactions loaded:", len(df))


# --------------------------------
# 3. Train Isolation Forest
# --------------------------------

model = IsolationForest(
    contamination=0.01,
    random_state=42
)

df["prediction"] = model.fit_predict(
    df[["AMOUNT"]]
)


# --------------------------------
# 4. Convert prediction
# --------------------------------

df["IS_ANOMALY"] = df["prediction"].apply(
    lambda x: "ANOMALY" if x == -1 else "NORMAL"
)

df.drop(columns=["prediction"], inplace=True)


# --------------------------------
# 5. Prepare data for Snowflake
# --------------------------------

df["TRANSACTION_DATE"] = pd.to_datetime(
    df["TRANSACTION_DATE"]
).dt.date

records = list(
    df[
        [
            "TRANSACTION_ID",
            "TRANSACTION_DATE",
            "CATEGORY",
            "MERCHANT",
            "AMOUNT",
            "PAYMENT_METHOD",
            "IS_ANOMALY"
        ]
    ].itertuples(index=False, name=None)
)


# --------------------------------
# 6. Clear previous ML results
# --------------------------------

cursor = conn.cursor()

cursor.execute("""
TRUNCATE TABLE EXPENSE_ANALYTICS_DB.ML.ANOMALIES
""")


# --------------------------------
# 7. Insert ML results
# --------------------------------

insert_query = """
INSERT INTO EXPENSE_ANALYTICS_DB.ML.ANOMALIES
(
    TRANSACTION_ID,
    TRANSACTION_DATE,
    CATEGORY,
    MERCHANT,
    AMOUNT,
    PAYMENT_METHOD,
    IS_ANOMALY
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, records)

print("ML results saved to Snowflake!")


# --------------------------------
# 8. Show anomaly count
# --------------------------------

anomaly_count = df[
    df["IS_ANOMALY"] == "ANOMALY"
].shape[0]

print("Anomalies detected:", anomaly_count)


# --------------------------------
# 9. Close connection
# --------------------------------

cursor.close()
conn.close()

print("Analysis completed successfully!")



