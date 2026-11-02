# Sales Performance Analysis & Business Insights Dashboard

An end-to-end Data Analyst portfolio project using Python, PostgreSQL, and Tableau. The project analyzes a fictional retail company's orders to understand sales performance, profitability, customer segments, discount patterns, and shipping efficiency.

## Business problem

Management needs clear answers to:
- Which regions and categories drive sales and profit?
- Which sub-categories lose money?
- How do sales and profit change month by month?
- How does discount level relate to profitability?
- Which customers contribute the most sales?
- How does delivery time vary by shipping mode?

## Tech stack

- Python: Pandas, NumPy, Matplotlib, Seaborn
- Database: PostgreSQL
- BI: Tableau
- Version control: Git and GitHub

## Dataset

Download the **Sample - Superstore.csv** dataset from:
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Place it at `data/Sample - Superstore.csv`.

This is sample/fictionalized retail data for learning and portfolio demonstration, not proprietary company data. The commonly shared CSV has approximately 10,000 line-item records. Verify the actual row count and date range after downloading.

## Repository structure

```text
sales-performance-analytics/
├── data/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── src/
│   ├── 01_clean_analyze.py
│   └── 02_load_postgres.py
├── sql/
│   └── analysis_queries.sql
├── tableau/
│   └── dashboard_build_guide.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/sales-performance-analytics.git
cd sales-performance-analytics
```

### 2. Create a virtual environment

Windows:
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Download the Kaggle CSV and place it in `data/` with the exact name:
`Sample - Superstore.csv`

### 5. Clean and analyze

```bash
python src/01_clean_analyze.py
```

This creates:
- `data/superstore_clean.csv`
- `reports/data_quality_report.txt`
- `reports/region_summary.csv`
- `reports/product_profitability.csv`
- `reports/monthly_trend.csv`
- `reports/eda_overview.png`

### 6. Configure PostgreSQL

Create a database named `superstore_db` in pgAdmin or psql.

Copy `.env.example` to `.env`, then update the local credentials. Never commit `.env`.

```bash
python src/02_load_postgres.py
```

The script loads the cleaned records into `public.sales_clean`.

### 7. Run SQL analysis

Open `sql/analysis_queries.sql` in pgAdmin Query Tool or run it with psql. It includes:
- KPI aggregation
- Region and product profitability
- Monthly trend analysis
- Discount band analysis
- Top customers
- Window-function ranking
- Shipping performance
- Tableau view creation

### 8. Build Tableau dashboard

Follow `tableau/dashboard_build_guide.md`. Connect Tableau to PostgreSQL and select `public.vw_sales_summary`.

Save the packaged workbook as:
`tableau/Sales_Performance_Dashboard.twbx`

## Key deliverables

- Reproducible Python data preparation and EDA scripts
- PostgreSQL analysis queries
- Tableau dashboard with executive, product, and customer/operations views
- Business recommendations based on measured results

## Analysis notes

- Dataset grain: one row represents an order line item, not necessarily one unique order. Use `COUNTD(Order ID)` for order counts.
- Profit can be negative. Do not remove negative-profit rows; they are important to the business problem.
- Profit margin should be calculated as `SUM(Profit) / SUM(Sales)`, not as an unweighted average of row-level margins.
- Discount association is not proof of causation. Describe it as an observed relationship.
- Do not write findings in this README until you have run the analysis and verified the actual outputs.

## Example business recommendations to evaluate

- Review high-discount product groups with weak or negative profit.
- Prioritize profitable product and regional combinations.
- Investigate regions with strong sales but low profit margins.
- Review shipping options where delivery time is high.

Only include recommendations that your actual analysis supports.

## GitHub upload

```bash
git init
git add .
git commit -m "Build end-to-end retail sales analytics project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/sales-performance-analytics.git
git push -u origin main
```

Before pushing, confirm that `.env`, raw customer-level data, and generated files you do not intend to share are excluded. Check `git status` and `git ls-files` before publishing.
