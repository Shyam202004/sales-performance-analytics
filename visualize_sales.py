
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Load database credentials
load_dotenv()

# Connect to PostgreSQL
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE")
)

engine = create_engine(connection_url)

# Load data
df = pd.read_sql(
    "SELECT * FROM vw_sales_summary",
    engine
)

# Create output folder
os.makedirs("reports/charts", exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Monthly Sales Trend
monthly_sales = (
    df.groupby("order_month_start")["sales"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 5))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values)
plt.title("Monthly Sales Trend (2014-2017)")
plt.xlabel("Month")
plt.ylabel("Sales (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/monthly_sales_trend.png", dpi=300)
plt.close()

# 2. Regional Sales
regional_sales = (
    df.groupby("region")["sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
sns.barplot(x=regional_sales.index, y=regional_sales.values)
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales (USD)")
plt.tight_layout()
plt.savefig("reports/charts/regional_sales.png", dpi=300)
plt.close()

# 3. Category Sales and Profit
category_data = (
    df.groupby("category")[["sales", "profit"]]
    .sum()
    .reset_index()
)

category_long = category_data.melt(
    id_vars="category",
    var_name="Metric",
    value_name="Amount"
)

plt.figure(figsize=(9, 5))
sns.barplot(
    data=category_long,
    x="category",
    y="Amount",
    hue="Metric"
)
plt.title("Sales and Profit by Category")
plt.xlabel("Category")
plt.ylabel("Amount (USD)")
plt.tight_layout()
plt.savefig("reports/charts/category_sales_profit.png", dpi=300)
plt.close()

# 4. Customer Segment Sales
segment_sales = (
    df.groupby("segment")["sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
sns.barplot(x=segment_sales.index, y=segment_sales.values)
plt.title("Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Sales (USD)")
plt.tight_layout()
plt.savefig("reports/charts/customer_segment_sales.png", dpi=300)
plt.close()

engine.dispose()

print("All visualizations created successfully!")
print("Charts saved in reports/charts/")
