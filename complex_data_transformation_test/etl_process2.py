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

# ETL Process: คำนวณยอดขายแยกตาม Location และ Gender
def calculate_user_location_sales(conn):
    query_clear = "TRUNCATE TABLE user_location_sales;"
    query_insert = """
        INSERT INTO user_location_sales (location, gender, total_sales, min_sales, max_sales, average_sales)
        SELECT 
            ui.location,
            ui.gender,
            SUM(t.quantity * t.amount) AS total_sales,
            MIN(t.quantity * t.amount) AS min_sales,
            MAX(t.quantity * t.amount) AS max_sales,
            AVG(t.quantity * t.amount) AS average_sales
        FROM transaction t
        JOIN user_info ui ON t.user_id = ui.user_id
        GROUP BY ui.location, ui.gender;
    """
    with conn.cursor() as cur:
        cur.execute(query_clear)  # Clear old data using TRUNCATE
        cur.execute(query_insert)  # Insert new data
    conn.commit()
    print("User location sales calculated and loaded successfully.")

# ETL Process: คำนวณ Top 20 สินค้าที่ขายดีที่สุดในเชียงใหม่
def calculate_top_products_in_Chiangmai(conn):
    query_clear = "TRUNCATE TABLE top_products_in_Chiangmai;"
    query_insert = """
        INSERT INTO top_products_in_Chiangmai (order_date, rank_num, product_id, total_sales, total_quantity)
        WITH ranked_products AS (
            SELECT 
                t.order_date,
                t.product_id,
                SUM(t.quantity * t.amount) AS total_sales,
                SUM(t.quantity) AS total_quantity,
                ROW_NUMBER() OVER (PARTITION BY t.order_date ORDER BY SUM(t.quantity * t.amount) DESC) AS rank_num
            FROM transaction t
            JOIN user_info ui ON t.user_id = ui.user_id
            WHERE ui.location = 'Chiangmai'
            GROUP BY t.order_date, t.product_id
        )
        SELECT order_date, rank_num, product_id, total_sales, total_quantity
        FROM ranked_products
        WHERE rank_num <= 20
        ORDER BY order_date, rank_num;
    """
    with conn.cursor() as cur:
        cur.execute(query_clear)  # Clear old data using TRUNCATE
        cur.execute(query_insert)  # Insert new data
    conn.commit()
    print("Top products in Chiangmai calculated and loaded successfully.")

# Main ETL Process
def main():
    conn = connect_db()
    try:
        print("Starting ETL Process for Question 3...")
        
        # Step 1: Calculate user location sales
        calculate_user_location_sales(conn)

        # Step 2: Calculate top products in Chiangmai
        calculate_top_products_in_Chiangmai(conn)

        print("ETL Process for Question 3 completed successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
