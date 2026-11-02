
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load database credentials from .env
load_dotenv()

# Read database settings
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE")
)

try:
    engine = create_engine(connection_url)

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM vw_sales_summary")
        )
        total_records = result.scalar()

        print("PostgreSQL connection successful!")
        print("Database:", os.getenv("PGDATABASE"))
        print("Total records:", total_records)

    engine.dispose()

except Exception as error:
    print("Database connection failed.")
    print("Error:", error)
