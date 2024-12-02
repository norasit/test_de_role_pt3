CREATE TABLE IF NOT EXISTS user_transaction_amount (
    user_id TEXT PRIMARY KEY,
    total_sales NUMERIC,
    average_sales NUMERIC
);
