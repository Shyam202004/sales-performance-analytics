
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

load_dotenv()

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE")
)

engine = create_engine(connection_url)

df = pd.read_sql(
    "SELECT * FROM vw_sales_summary",
    engine
)

# Overall business performance
print("\n--- BUSINESS PERFORMANCE ---")
print("Total Sales:", round(df["sales"].sum(), 2))
print("Total Profit:", round(df["profit"].sum(), 2))
print("Total Orders:", df["order_id"].nunique())
print("Total Customers:", df["customer_id"].nunique())
print("Total Products:", df["product_id"].nunique())
print("Total Quantity Sold:", df["quantity"].sum())

# Regional sales
print("\n--- REGIONAL SALES ---")
print(
    df.groupby("region")["sales"]
    .sum()
    .sort_values(ascending=False)
)

# Category sales
print("\n--- CATEGORY SALES ---")
print(
    df.groupby("category")["sales"]
    .sum()
    .sort_values(ascending=False)
)

# Category profit
print("\n--- CATEGORY PROFIT ---")
print(
    df.groupby("category")["profit"]
    .sum()
    .sort_values(ascending=False)
)

engine.dispose()

# Customer segment analysis
print("\n--- CUSTOMER SEGMENT SALES ---")
print(
    df.groupby("segment")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- CUSTOMER SEGMENT PROFIT ---")
print(
    df.groupby("segment")["profit"]
    .sum()
    .sort_values(ascending=False)
)

# Monthly sales trend
print("\n--- YEARLY SALES ---")
print(
    df.groupby("order_year")["sales"]
    .sum()
    .round(2)
)

engine.dispose()


# Monthly sales analysis
print("\n--- MONTHLY SALES ANALYSIS ---")

monthly_sales = (
    df.groupby("order_month_start")["sales"]
    .sum()
    .sort_index()
)

print(monthly_sales.round(2))

# Top 5 sales months
print("\n--- TOP 5 SALES MONTHS ---")

print(
    monthly_sales
    .sort_values(ascending=False)
    .head(5)
    .round(2)
)

# Year-wise profit
print("\n--- YEARLY PROFIT ---")

print(
    df.groupby("order_year")["profit"]
    .sum()
    .round(2)
)
