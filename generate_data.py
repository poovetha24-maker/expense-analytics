import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

categories = {
    "Food": ["Swiggy", "Zomato", "Restaurant", "Cafe"],
    "Transport": ["Uber", "Ola", "Bus", "Petrol"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Local Store"],
    "Bills": ["Electricity", "Internet", "Mobile", "Water"],
    "Education": ["College", "Udemy", "Book Store", "Coursera"],
    "Entertainment": ["Netflix", "Movie", "Spotify", "Games"],
    "Healthcare": ["Pharmacy", "Hospital", "Clinic"],
    "Travel": ["IRCTC", "Flight", "Hotel", "Travel Agency"]
}

payment_methods = ["UPI", "Card", "Cash", "Net Banking"]

descriptions = {
    "Food": "Food expense",
    "Transport": "Transportation expense",
    "Shopping": "Shopping expense",
    "Bills": "Monthly bill",
    "Education": "Education expense",
    "Entertainment": "Entertainment expense",
    "Healthcare": "Healthcare expense",
    "Travel": "Travel expense"
}

rows = []

start_date = datetime(2026, 1, 1)

for i in range(2000):

    category = random.choice(list(categories.keys()))
    merchant = random.choice(categories[category])

    date = start_date + timedelta(days=random.randint(0, 364))

    # Normal spending ranges
    ranges = {
        "Food": (80, 1200),
        "Transport": (40, 1000),
        "Shopping": (300, 8000),
        "Bills": (300, 4000),
        "Education": (200, 5000),
        "Entertainment": (100, 2500),
        "Healthcare": (200, 6000),
        "Travel": (1000, 15000)
    }

    low, high = ranges[category]

    amount = round(random.uniform(low, high), 2)

    payment_method = random.choice(payment_methods)

    rows.append([
        f"T{i+1:05d}",
        date.strftime("%Y-%m-%d"),
        category,
        merchant,
        amount,
        payment_method,
        descriptions[category]
    ])


# Add unusual transactions for anomaly detection
anomalies = [
    ["T02001", "2026-03-15", "Food", "Restaurant", 25000, "Card", "Unusually high food expense"],
    ["T02002", "2026-05-20", "Shopping", "Amazon", 75000, "Card", "Unusually high shopping expense"],
    ["T02003", "2026-07-11", "Transport", "Uber", 18000, "UPI", "Unusually high transport expense"],
    ["T02004", "2026-09-05", "Entertainment", "Games", 30000, "Card", "Unusually high entertainment expense"],
    ["T02005", "2026-11-22", "Food", "Restaurant", 22000, "UPI", "Unusually high food expense"]
]

rows.extend(anomalies)

columns = [
    "transaction_id",
    "transaction_date",
    "category",
    "merchant",
    "amount",
    "payment_method",
    "description"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("transactions.csv", index=False)

print("Dataset generated successfully!")
print("Rows:", len(df))
print("\nFirst 5 rows:")
print(df.head())