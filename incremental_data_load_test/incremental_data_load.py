import os
import psycopg2
import pandas as pd

# Database connection settings
DB_HOST = "postgres"
DB_NAME = "my_db"
DB_USER = "postgres_user"
DB_PASSWORD = "postgres_password"
CSV_DIR = "/data/sales"

# Connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Check which files have already been loaded
def get_loaded_files(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT file_name FROM meta_data")
        return {row[0] for row in cur.fetchall()}

# Load a CSV file into the database
def load_csv_to_db(conn, csv_file):
    df = pd.read_csv(csv_file)
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO transaction (order_id, user_id, product_id, quantity, amount, order_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
            """, (row['order_id'], row['user_id'], row['product_id'], row['quantity'], row['amount'], row['order_date']))
        # Record the file as processed
        cur.execute("INSERT INTO meta_data (file_name) VALUES (%s)", (os.path.basename(csv_file),))
    conn.commit()

# Main incremental load function
def incremental_load():
    conn = connect_db()
    try:
        # Ensure meta_data table exists
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS meta_data (
                    file_name TEXT PRIMARY KEY,
                    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()

        loaded_files = get_loaded_files(conn)
        csv_files = [os.path.join(CSV_DIR, f) for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

        for csv_file in csv_files:
            if os.path.basename(csv_file) not in loaded_files:
                print(f"Loading file: {csv_file}")
                load_csv_to_db(conn, csv_file)
            else:
                print(f"File already loaded: {csv_file}")

    finally:
        conn.close()

if __name__ == "__main__":
    incremental_load()
