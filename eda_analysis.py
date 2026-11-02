
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Load environment variables
load_dotenv()

# PostgreSQL connection
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

# 1. Dataset shape
print("\n--- DATASET SHAPE ---")
print(df.shape)

# 2. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 3. Duplicate records
print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

# 4. Column data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 5. Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(df.describe())

engine.dispose()
