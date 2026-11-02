
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Load environment variables
load_dotenv()

# Create PostgreSQL connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE")
)

engine = create_engine(connection_url)

# Load data from PostgreSQL
query = "SELECT * FROM vw_sales_summary"

df = pd.read_sql(query, engine)

# Display dataset information
print("Data loaded successfully!")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nFirst 5 records:")
print(df.head())

engine.dispose()
