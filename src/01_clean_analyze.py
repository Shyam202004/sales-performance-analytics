from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

# Place the Kaggle file in data/ and keep this filename.
INPUT_FILE = DATA_DIR / "Sample - Superstore.csv"
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}\n"
        "Download Sample - Superstore.csv and place it in the data/ folder."
    )

# The commonly shared Superstore CSV is encoded in latin-1.
df = pd.read_csv(INPUT_FILE, encoding="latin-1")
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# Convert known date and numeric columns safely.
for col in ["order_date", "ship_date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

numeric_cols = ["row_id", "postal_code", "sales", "quantity", "discount", "profit"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

required = [
    "order_id", "order_date", "customer_id", "region",
    "category", "sales", "quantity", "profit"
]
missing_columns = [c for c in required if c not in df.columns]
if missing_columns:
    raise ValueError(f"Missing expected columns: {missing_columns}. Found: {list(df.columns)}")

# Data-quality checks before removing anything.
quality_lines = [
    f"Rows before cleaning: {len(df):,}",
    f"Duplicate rows: {int(df.duplicated().sum()):,}",
    "Missing values by column:",
    df.isna().sum().to_string(),
]

# Remove exact duplicate records. Keep records with missing postal codes;
# postal_code is not required for the core analysis.
df = df.drop_duplicates().copy()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
if "ship_date" in df.columns:
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# Drop records that cannot support core sales analysis.
df = df.dropna(subset=["order_id", "order_date", "customer_id", "sales", "profit"])
df = df[df["quantity"].fillna(0) > 0].copy()

# Standardize text fields without changing business meaning.
for col in ["region", "category", "sub_category", "segment", "ship_mode"]:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip()

df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["order_month_name"] = df["order_date"].dt.strftime("%b")
df["order_month_start"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
df["profit_margin"] = np.where(df["sales"] != 0, df["profit"] / df["sales"], np.nan)
if "ship_date" in df.columns:
    df["delivery_days"] = (df["ship_date"] - df["order_date"]).dt.days
    df.loc[df["delivery_days"] < 0, "delivery_days"] = np.nan

# Save clean data and reproducibility reports.
clean_file = DATA_DIR / "superstore_clean.csv"
df.to_csv(clean_file, index=False)
quality_lines += [
    "",
    f"Rows after cleaning: {len(df):,}",
    f"Rows removed: {int(len(pd.read_csv(INPUT_FILE, encoding='latin-1')) - len(df)):,}",
    f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}",
]
(REPORT_DIR / "data_quality_report.txt").write_text("\n".join(quality_lines), encoding="utf-8")

# Export summary tables for validation and optional Tableau CSV use.
df.groupby("region", as_index=False).agg(
    sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")
).sort_values("sales", ascending=False).to_csv(REPORT_DIR / "region_summary.csv", index=False)

df.groupby(["category", "sub_category"], as_index=False).agg(
    sales=("sales", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum")
).sort_values("profit").to_csv(REPORT_DIR / "product_profitability.csv", index=False)

monthly = df.groupby("order_month_start", as_index=False).agg(
    sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")
)
monthly.to_csv(REPORT_DIR / "monthly_trend.csv", index=False)

# A compact EDA chart saved for the README / portfolio.
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
region = df.groupby("region")["sales"].sum().sort_values()
region.plot(kind="barh", ax=axes[0], title="Sales by Region")
product = df.groupby("sub_category")["profit"].sum().sort_values()
product.plot(kind="barh", ax=axes[1], title="Profit by Sub-Category")
axes[0].set_xlabel("Sales")
axes[1].set_xlabel("Profit")
fig.tight_layout()
fig.savefig(REPORT_DIR / "eda_overview.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Cleaned dataset saved: {clean_file}")
print(f"Rows retained: {len(df):,}")
print(f"Reports saved in: {REPORT_DIR}")
