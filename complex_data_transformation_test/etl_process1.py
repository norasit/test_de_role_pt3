import psycopg2

# Database connection settings
DB_HOST = "postgres"
DB_NAME = "my_db"
DB_USER = "postgres_user"
DB_PASSWORD = "postgres_password"

# Connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# ETL Process: คำนวณ Total และ Average Sales ต่อผู้ใช้
def calculate_user_transaction_amount(conn):
    query_clear = "TRUNCATE TABLE user_transaction_amount;"
    query_insert = """
        INSERT INTO user_transaction_amount (user_id, total_sales, average_sales)
        SELECT 
            user_id, 
            SUM(quantity * amount) AS total_sales, 
            AVG(quantity * amount) AS average_sales
        FROM transaction
        GROUP BY user_id;
    """
    with conn.cursor() as cur:
        cur.execute(query_clear)  # Clear old data using TRUNCATE
        cur.execute(query_insert)  # Insert new data
    conn.commit()
    print("User transaction amount calculated and loaded successfully.")

# ETL Process: คำนวณ Total, Min, Max, Average Sales และ VAT รายวัน
def calculate_daily_transaction_amount(conn):
    query_clear = "TRUNCATE TABLE daily_transaction_amount;"
    query_insert = """
        INSERT INTO daily_transaction_amount (order_date, total_sales, min_sales, max_sales, average_sales, vat)
        SELECT 
            order_date,
            SUM(quantity * amount) AS total_sales,
            MIN(quantity * amount) AS min_sales,
            MAX(quantity * amount) AS max_sales,
            AVG(quantity * amount) AS average_sales,
            SUM(quantity * amount) * 0.07 AS vat
        FROM transaction
        GROUP BY order_date;
    """
    with conn.cursor() as cur:
        cur.execute(query_clear)  # Clear old data using TRUNCATE
        cur.execute(query_insert)  # Insert new data
    conn.commit()
    print("Daily transaction amount calculated and loaded successfully.")

# ETL Process: คำนวณจำนวน Transaction และ Total Sales ต่อสินค้า
def calculate_product_sales(conn):
    query_clear = "TRUNCATE TABLE product_sales;"
    query_insert = """
        INSERT INTO product_sales (product_id, total_quantity, total_sales)
        SELECT 
            product_id,
            SUM(quantity) AS total_quantity,
            SUM(quantity * amount) AS total_sales
        FROM transaction
        GROUP BY product_id;
    """
    with conn.cursor() as cur:
        cur.execute(query_clear)  # Clear old data using TRUNCATE
        cur.execute(query_insert)  # Insert new data
    conn.commit()
    print("Product sales calculated and loaded successfully.")

# Main ETL Process
def main():
    conn = connect_db()
    try:
        print("Starting ETL Process...")
        
        # Step 1: Calculate user transaction amount
        calculate_user_transaction_amount(conn)

        # Step 2: Calculate daily transaction amount
        calculate_daily_transaction_amount(conn)

        # Step 3: Calculate product sales
        calculate_product_sales(conn)

        print("ETL Process completed successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
