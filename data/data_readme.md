Dataset Overview -:

This dataset simulates Netflix’s global revenue, subscribers, and growth metrics from January 2022 to December 2024 across four major regions and three subscription plans.
The goal is to enable exploratory data analysis, anomaly detection, and strategic insight generation for the project

File Details -:

Filename: netflix_global_revenue.csv
Location: /data/netflix_global_revenue.csv
Rows: ~432 (3 years × 12 months × 4 regions × 3 plans)
File Format: CSV (UTF-8 encoded)

| Column Name              | Type               | Example                                     | Description                                                     |
| ------------------------ | ------------------ | ------------------------------------------- | --------------------------------------------------------------- |
| `date`                   | Date (YYYY-MM-DD)  | `2023-04-01`                                | Monthly timestamp of recorded metrics                           |
| `region`                 | String             | `APAC` / `North America` / `EMEA` / `LATAM` | Netflix operating region                                        |
| `subscription_plan`      | String             | `Basic`, `Standard`, `Premium`              | Subscription plan type                                          |
| `revenue_usd_mn`         | Float              | `845.2`                                     | Total revenue (in USD millions) for that region-plan-month      |
| `subscribers_mn`         | Float              | `62.4`                                      | Number of paid subscribers (in millions)                        |
| `growth_rate`            | Float (percentage) | `4.3`                                       | Month-over-month revenue growth (%)                             |
| `content_launch`         | String             | `Stranger Things S4` / `N/A`                | Notable content event or major release driving growth           |
| `marketing_spend_usd_mn` | Float              | `35.6`                                      | Estimated marketing investment (in USD millions) that month     |
| `adoption_rate`          | Float              | `0.72`                                      | Ratio of new users to total potential market for that region    |
| `anomalies`              | Integer (0 or 1)   | `1`                                         | Machine learning label — 1 = anomaly detected, 0 = normal trend |
| `retention_index`        | Float              | `0.86`                                      | Estimated percentage of retained subscribers (1 = 100%)         |


Data Generation Logic -:

Data generated using Python (numpy, pandas, random) to ensure realistic seasonality and variance.
Revenue and subscriber trends increase over time with random fluctuations.
Spikes and dips correspond to content launches or market anomalies.
Growth rate and retention indices are computed to simulate actual performance metrics.
5-10% of records are marked as anomalies to represent irregularities in business performance.

Business Use Cases -:

This dataset is designed to:
Monitor regional and plan-wise revenue trends over time.
Detect anomalies (sudden drops/spikes) via ML (IsolationForest).
Support executive storytelling e.g., linking growth to launches or regional factors.
Enable strategy recommendations like pricing optimization, retention focus, or release scheduling.

Data Notes -:

This is a synthetic dataset created for project purpose.
No confidential or proprietary Netflix data has been used.
Values are scaled and randomized within realistic bounds based on public Netflix financial disclosures and regional performance insights.
