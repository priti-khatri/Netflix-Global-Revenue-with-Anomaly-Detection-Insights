import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Parameters
regions = ["North America", "Latin America", "Europe", "APAC", "Middle East & Africa"]
plans = ["Basic", "Standard", "Premium"]

start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 11, 1)
dates = pd.date_range(start_date, end_date, freq='MS')

data = []

for region in regions:
    base_revenue = random.randint(200, 1000) * 1e6  # Base revenue in millions
    for plan in plans:
        for date in dates:
            growth = np.random.normal(1.005, 0.015)  # avg 0.5% monthly growth
            base_revenue *= growth
            # Introduce random anomalies
            if random.random() < 0.03:
                base_revenue *= np.random.choice([0.8, 1.2])  # sudden drop/spike
            subscribers = base_revenue / np.random.uniform(10, 20)
            data.append([date, region, plan, round(base_revenue, 2), int(subscribers)])

df = pd.DataFrame(data, columns=["Date", "Region", "Plan", "Revenue", "Subscribers"])
df.to_csv("data/netflix_global_revenue.csv", index=False)

print("✅ Synthetic dataset generated and saved as netflix_global_revenue.csv")
