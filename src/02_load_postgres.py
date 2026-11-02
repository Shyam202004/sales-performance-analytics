from pathlib import Path
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

csv_path = ROOT / "data" / "superstore_clean.csv"
if not csv_path.exists():
    raise FileNotFoundError("Run src/01_clean_analyze.py first.")

required_env = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
missing = [key for key in required_env if not os.getenv(key)]
if missing:
    raise EnvironmentError(f"Missing .env values: {missing}. Copy .env.example to .env and update it.")

url = (
    f"postgresql+psycopg2://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}"
    f"@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)
engine = create_engine(url)

df = pd.read_csv(csv_path, parse_dates=["order_date", "ship_date", "order_month_start"])
# to_sql creates/replaces a convenient analysis table. Do not run this against
# a production database; this project uses a dedicated local practice database.
with engine.begin() as conn:
    df.to_sql("sales_clean", conn, if_exists="replace", index=False, method="multi", chunksize=1000)
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales_clean (order_date);
        CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_clean (region);
        CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_clean (product_id);
    """))

print(f"Loaded {len(df):,} rows into PostgreSQL table public.sales_clean")
print("Next: run sql/analysis_queries.sql in pgAdmin or psql.")
