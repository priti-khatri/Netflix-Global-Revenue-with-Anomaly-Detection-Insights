import pandas as pd
import numpy as np
import sklearn
import os
from datetime import datetime
from sklearn.ensemble import IsolationForest

# CONFIGURATION

np.random.seed(42)

regions = ["North America", "EMEA", "APAC", "LATAM"]
plans = ["Basic", "Standard", "Premium"]
start_date = "2022-01-01"
end_date = "2024-12-01"

# Make sure data folder exists
os.makedirs("data", exist_ok=True)


# GENERATE DATE RANGE

dates = pd.date_range(start=start_date, end=end_date, freq="MS")


# BASE PARAMETERS

region_base_revenue = {
    "North America": 900,
    "EMEA": 600,
    "APAC": 400,
    "LATAM": 250
}

plan_multiplier = {
    "Basic": 0.7,
    "Standard": 1.0,
    "Premium": 1.4
}

marketing_baseline = {
    "North America": 40,
    "EMEA": 30,
    "APAC": 25,
    "LATAM": 20
}

content_events = {
    "2022-03": "Stranger Things S4",
    "2022-11": "The Crown S5",
    "2023-05": "Money Heist Korea",
    "2023-10": "Lupin S3",
    "2024-06": "Bridgerton S3",
    "2024-09": "Squid Game S2"
}


# GENERATE DATA
data = []

for region in regions:
    for plan in plans:
        base_rev = region_base_revenue[region] * plan_multiplier[plan]
        subs_base = (base_rev / 10) + np.random.randint(20, 60)
        marketing_base = marketing_baseline[region]

        for date in dates:
            # Seasonal adjustment (simulate higher Q4 performance)
            month = date.month
            seasonality = 1 + (0.1 if month in [10, 11, 12] else 0)

            # Random growth trend
            growth = np.random.normal(0.03, 0.02)

            # Revenue calculation
            revenue = base_rev * seasonality * (1 + growth)
            revenue += np.random.normal(0, 25)

            # Subscribers proportional to revenue
            subscribers = subs_base * (1 + growth * 0.8)
            subscribers += np.random.normal(0, 3)

            # Marketing spend
            marketing_spend = marketing_base * (1 + np.random.normal(0.05, 0.03))

            # Adoption rate (randomized between 0.6–0.9)
            adoption_rate = np.clip(np.random.normal(0.75, 0.07), 0.5, 0.95)

            # Retention index (higher for Premium, lower for Basic)
            retention_index = np.clip(0.8 + (0.05 if plan == "Premium" else -0.05 if plan == "Basic" else 0)
                                      + np.random.normal(0, 0.02), 0.6, 0.95)

            # Content event (if applicable)
            event_key = f"{date.year}-{str(date.month).zfill(2)}"
            content_launch = content_events.get(event_key, "N/A")

            data.append({
                "date": date,
                "region": region,
                "subscription_plan": plan,
                "revenue_usd_mn": round(revenue, 2),
                "subscribers_mn": round(subscribers, 2),
                "growth_rate": round(growth * 100, 2),
                "content_launch": content_launch,
                "marketing_spend_usd_mn": round(marketing_spend, 2),
                "adoption_rate": round(adoption_rate, 2),
                "retention_index": round(retention_index, 2)
            })

df = pd.DataFrame(data)


# ADD ANOMALIES USING ISOLATION FOREST

model = IsolationForest(contamination=0.05, random_state=42)
df["anomalies"] = model.fit_predict(df[["revenue_usd_mn", "subscribers_mn", "growth_rate"]])
df["anomalies"] = df["anomalies"].apply(lambda x: 1 if x == -1 else 0)


# SAVE TO CSV

output_path = "data/netflix_global_revenue.csv"
df.to_csv(output_path, index=False)
print(f" Dataset generated and saved to: {output_path}")
print(df.head(10))
