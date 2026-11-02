# Sales Performance Analysis & Business Insights Dashboard

An end-to-end Data Analyst portfolio project using Python, PostgreSQL, SQL, and Tableau. This project analyzes a fictional retail company's sales data to identify business trends, evaluate profitability, understand customer segments, examine discount patterns, and analyze shipping performance.

## Project Overview

The objective of this project is to transform raw retail sales data into meaningful business insights using data cleaning, exploratory data analysis, SQL queries, and interactive visualization.

## Business Problems

This project answers the following business questions:

- Which regions generate the highest sales and profit?
- Which product categories and sub-categories are most profitable?
- Which products or sub-categories generate losses?
- How do sales and profit change over time?
- How do discount levels relate to profitability?
- Who are the top customers based on sales?
- How does delivery performance vary by shipping mode?

## Tech Stack

- **Programming:** Python
- **Python Libraries:** Pandas, NumPy, Matplotlib, Seaborn
- **Database:** PostgreSQL
- **Query Language:** SQL
- **Business Intelligence:** Tableau
- **Tools:** VS Code, pgAdmin, Git, GitHub

## Dataset

**Dataset:** Sample Superstore Dataset

Source: [Kaggle – Sample Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

The dataset contains fictionalized retail sales information, including orders, customers, products, sales, profit, discounts, regions, and shipping details.

The original CSV is not included in this GitHub repository. Download it and place it inside the `data/` folder.

Expected filename: `Sample - Superstore.csv`

## Project Structure

```text
sales-performance-analytics/
│
├── data/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
├── src/
│   ├── 01_clean_analyze.py
│   └── 02_load_postgres.py
│
├── sql/
│   └── analysis_queries.sql
│
├── tableau/
│   ├── README.txt
│   └── dashboard_build_guide.md
│
├── business_insights.py
├── eda_analysis.py
├── load_data.py
├── test_db_connection.py
├── visualize_sales.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Project Workflow

### 1. Data Collection

Downloaded the Sample Superstore dataset from Kaggle and prepared it for analysis.

### 2. Data Cleaning and Exploratory Data Analysis

Used Python and Pandas to examine the dataset, check missing values, identify duplicate records, inspect data types, and understand the overall data structure.

### 3. PostgreSQL Database Integration

Created a PostgreSQL database named `sales_analytics` and loaded the sales records into the `public.sales_clean` table.

Used SQLAlchemy, psycopg2, and python-dotenv for database connectivity.

### 4. SQL Analysis

Created SQL queries to analyze:

- Overall business KPIs
- Regional sales and profitability
- Category and sub-category performance
- Monthly sales trends
- Discount and profit relationships
- Top 10 customers
- Top 5 products by region using window functions
- Shipping performance
- Summary view for Tableau

### 5. Data Visualization

Used Python Matplotlib to generate charts for:

- Monthly sales trends
- Regional sales performance
- Category sales and profit
- Customer segment sales

### 6. Tableau Dashboard

Developed and published an interactive dashboard containing KPI summaries, monthly sales trends, regional performance, category analysis, profit analysis, and top-performing products.

**View the published dashboard:**

[Sales Performance Analysis Dashboard – Tableau Public](https://public.tableau.com/app/profile/shyam.b7714/viz/SalesPerformanceAnalysisDashboard_17936272431160/SalesPerformanceDashboard)

## Key Business Insights

The following findings were obtained from the completed analysis:

| Business Metric | Result |
|---|---:|
| Total Sales | $2,297,200.86 |
| Total Profit | $286,397.02 |
| Profit Margin | 12.47% |
| Total Orders | 5,009 |
| Unique Customers | 793 |
| Unique Products | 1,862 |
| Units Sold | 37,873 |

### Important Findings

- The West region generated the highest sales, approximately $725,457.82.
- Technology generated the highest category profit, approximately $145,454.95.
- Furniture Tables recorded a loss of approximately $17,725.48.
- Discounts above 30% were associated with a total loss of approximately $125,006.78.
- Consumer customers contributed the highest sales among the customer segments.
- Annual sales increased from approximately $484,247.50 in 2014 to $733,215.26 in 2017.

### Business Recommendations

- Review high-discount products that generate negative profit.
- Focus on improving the profitability of the Furniture category.
- Analyze regional differences in sales and profit margins.
- Identify opportunities to improve customer retention and sales.
- Monitor shipping performance across different shipping modes.

These recommendations are based on observed patterns in the sample dataset. Discount relationships should not be interpreted as proof of causation.

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Shyam202004/sales-performance-analytics.git
cd sales-performance-analytics
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset

Download the Sample Superstore CSV from Kaggle and place it inside the `data/` folder.

### 5. Configure PostgreSQL

Create a PostgreSQL database named:

```text
sales_analytics
```

Copy `.env.example` to `.env` and configure your local PostgreSQL connection details.

Never upload your actual `.env` file or database password to GitHub.

### 6. Run the Python Scripts

```bash
python test_db_connection.py
python load_data.py
python eda_analysis.py
python business_insights.py
python visualize_sales.py
```

### 7. Execute SQL Queries

Open `sql/analysis_queries.sql` in pgAdmin Query Tool and execute the queries to explore sales performance and business insights.

### 8. View the Tableau Dashboard

Open the published dashboard:

[View Sales Performance Dashboard](https://public.tableau.com/app/profile/shyam.b7714/viz/SalesPerformanceAnalysisDashboard_17936272431160/SalesPerformanceDashboard)

## Important Analysis Notes

- Each dataset row represents an order line item, not necessarily a unique order.
- Use distinct order counts when calculating total orders.
- Negative-profit records are retained because they are important for profitability analysis.
- Overall profit margin is calculated using total profit divided by total sales.
- Discount relationships indicate association, not necessarily causation.
- The dataset is fictionalized sample data and does not represent actual company financial information.

## Skills Demonstrated

- Python Programming
- Data Cleaning and Exploratory Data Analysis
- SQL Query Writing
- PostgreSQL Database Management
- Data Visualization
- Tableau Dashboard Development
- Business Intelligence and Analytical Thinking
- Git and GitHub Version Control

## Author

**Shyam B**

GitHub: [https://github.com/Shyam202004](https://github.com/Shyam202004)

Project Repository: [Sales Performance Analytics](https://github.com/Shyam202004/sales-performance-analytics)
