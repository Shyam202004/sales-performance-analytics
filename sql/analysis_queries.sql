-- Sales Performance Analysis | PostgreSQL
-- Run after src/02_load_postgres.py has created public.sales_clean.

-- 1. Executive KPI summary
SELECT
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0) * 100)::numeric, 2) AS profit_margin_pct,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM sales_clean;

-- 2. Sales and profit by region
SELECT region,
       ROUND(SUM(sales)::numeric, 2) AS sales,
       ROUND(SUM(profit)::numeric, 2) AS profit,
       ROUND((SUM(profit) / NULLIF(SUM(sales), 0) * 100)::numeric, 2) AS margin_pct
FROM sales_clean
GROUP BY region
ORDER BY sales DESC;

-- 3. Category and sub-category profitability (loss-making items first)
SELECT category, sub_category,
       ROUND(SUM(sales)::numeric, 2) AS sales,
       ROUND(SUM(profit)::numeric, 2) AS profit,
       ROUND((SUM(profit) / NULLIF(SUM(sales), 0) * 100)::numeric, 2) AS margin_pct
FROM sales_clean
GROUP BY category, sub_category
ORDER BY profit ASC;

-- 4. Monthly sales trend
SELECT DATE_TRUNC('month', order_date)::date AS month,
       ROUND(SUM(sales)::numeric, 2) AS sales,
       ROUND(SUM(profit)::numeric, 2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales_clean
GROUP BY 1
ORDER BY 1;

-- 5. Discount band analysis. Compare average line-item profit and total profit.
SELECT
    CASE
        WHEN discount = 0 THEN '0%'
        WHEN discount <= 0.10 THEN '1-10%'
        WHEN discount <= 0.20 THEN '11-20%'
        WHEN discount <= 0.30 THEN '21-30%'
        ELSE 'Above 30%'
    END AS discount_band,
    COUNT(*) AS line_items,
    ROUND(AVG(profit)::numeric, 2) AS avg_line_profit,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    ROUND(AVG(discount)::numeric, 3) AS avg_discount
FROM sales_clean
GROUP BY 1
ORDER BY MIN(discount);

-- 6. Top 10 customers by sales
WITH customer_sales AS (
    SELECT customer_id, MAX(customer_name) AS customer_name,
           SUM(sales) AS total_sales, SUM(profit) AS total_profit
    FROM sales_clean
    GROUP BY customer_id
)
SELECT customer_id, customer_name,
       ROUND(total_sales::numeric, 2) AS total_sales,
       ROUND(total_profit::numeric, 2) AS total_profit,
       RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 10;

-- 7. Top 5 products within each region using a window function
WITH product_region AS (
    SELECT region, product_id, MAX(product_name) AS product_name,
           SUM(sales) AS total_sales,
           RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS product_rank
    FROM sales_clean
    GROUP BY region, product_id
)
SELECT region, product_id, product_name,
       ROUND(total_sales::numeric, 2) AS total_sales, product_rank
FROM product_region
WHERE product_rank <= 5
ORDER BY region, product_rank;

-- 8. Shipping performance
SELECT ship_mode,
       ROUND(AVG(delivery_days)::numeric, 2) AS avg_delivery_days,
       COUNT(DISTINCT order_id) AS orders
FROM sales_clean
WHERE delivery_days IS NOT NULL
GROUP BY ship_mode
ORDER BY avg_delivery_days;

-- 9. Create a Tableau-friendly view with consistent business metrics
CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
    row_id, order_id, order_date, ship_date, ship_mode,
    customer_id, customer_name, segment, country, city, state,
    postal_code, region, product_id, category, sub_category,
    product_name, sales, quantity, discount, profit,
    order_year, order_month, order_month_name, order_month_start,
    profit_margin, delivery_days
FROM sales_clean;

-- 10. Sanity check: the view should contain the same number of records.
SELECT COUNT(*) AS view_rows FROM vw_sales_summary;


