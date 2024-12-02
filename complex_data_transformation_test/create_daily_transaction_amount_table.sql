CREATE TABLE IF NOT EXISTS daily_transaction_amount (
    order_date DATE PRIMARY KEY,
    total_sales NUMERIC,
    min_sales NUMERIC,
    max_sales NUMERIC,
    average_sales NUMERIC,
    vat NUMERIC
);
