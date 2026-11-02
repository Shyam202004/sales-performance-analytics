# Tableau Dashboard Build Guide

Connect Tableau Desktop to PostgreSQL:
- Server: `localhost`
- Port: `5432`
- Database: `superstore_db`
- Schema: `public`
- Table/view: `vw_sales_summary`
- Sign in with your local PostgreSQL username and password.

Tableau's PostgreSQL connector may require its database driver. Install the driver if Tableau prompts you.

## Calculated fields

Create these calculated fields in Tableau:

**Profit Margin**
```tableau
SUM([Profit]) / SUM([Sales])
```

**Order Count**
```tableau
COUNTD([Order Id])
```

**Average Order Value**
```tableau
SUM([Sales]) / COUNTD([Order Id])
```

**Year-Month**
```tableau
DATETRUNC('month', [Order Date])
```

Format Profit Margin as Percentage and Sales/Profit as currency.

## Dashboard 1 — Executive Overview

Recommended layout (top to bottom):
1. Title: Sales Performance Overview
2. KPI cards: Total Sales, Total Profit, Profit Margin, Orders, Units Sold
3. Line chart: monthly sales trend (Year-Month on Columns, SUM(Sales) on Rows)
4. Horizontal bar chart: sales by region, with profit in color or tooltip
5. Bar chart: profit by category
6. Filters: Order Date, Region, Segment, Category

## Dashboard 2 — Product & Discount Analysis

1. Bar chart: profit by sub-category, sorted ascending (losses appear first)
2. Scatter plot: Discount vs Profit; add Category to Color and Sales to Size
3. Bar chart: top 10 products by sales
4. Table: category, sub-category, sales, profit, profit margin
5. Filters: Region, Category, Segment

## Dashboard 3 — Customer & Operations

1. Bar chart: sales and profit by customer segment
2. Top 10 customers by sales table
3. Bar chart: average delivery days by ship mode
4. Map: sales by State (optional)
5. Filters: Order Date, Region, Segment

## Interactivity and polish

- Add dashboard filter actions so selecting a region filters the other charts.
- Use informative tooltips with Sales, Profit, Profit Margin, and Orders.
- Use consistent number formats and a restrained color palette.
- Add a subtitle explaining that this is a sample retail dataset.
- Validate dashboard totals against SQL query 1 before publishing.
- Save the workbook as `tableau/Sales_Performance_Dashboard.twbx`.
