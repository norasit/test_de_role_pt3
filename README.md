# Data Engineer Tests Part3

This project involves running an ETL process using Python scripts and SQL scripts for creating and populating tables in a PostgreSQL database. The project uses **Docker** for a consistent and portable environment setup.

**Note**: If you don't have Docker installed, you can head over to the [Get Docker](https://docs.docker.com/get-docker/) page for installation instructions.

## Getting Started

### 1. Clone the repository
```
git clone https://github.com/norasit/test_de_role_pt3.git
```
```
cd test_de_role_pt3
```

### 2. Using Docker
**Build and Start the Docker services**
1. Build and start the services (PostgreSQL, pgAdmin, and Python environment):
```
docker compose up --build
```

2. Verify services:
- PostgreSQL: The database will be accessible at localhost:5432.
- pgAdmin: Open your browser and go to http://localhost:5050.
- Login credentials:
  - **Email**: `admin@example.com`
  - **Password**: `admin1234`

### 3. Setting up the Database
Run the following commands to create and populate the necessary tables in PostgreSQL:

1. **Create the base schema and tables**:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /data/create_schema.sql
```

2. **Insert data from 'user_info.csv' into the table**:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /data/insert_data.sql
```

3. **Incremental data load, create transaction table and meta table**:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/incremental/create_transaction_table.sql
```
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/incremental/create_meta_table.sql
```

4. **Insert data from 'ref/sales/*.csv' into the transaction table**:
```
docker exec -it python_container python /scripts/incremental/incremental_data_load.py
```

5. **Create additional tables for ETL processing**:
- user_transaction_amount:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/complex/create_user_transaction_amount_table.sql
```
- daily_transaction_amount:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/complex/create_daily_transaction_amount_table.sql
```
- product_sales:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/complex/create_product_sales_table.sql
```
- user_location_sales:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/complex/create_user_location_sales_table.sql
```
- top_products_in_Chiangmai:
```
docker exec -i postgres psql -U postgres_user -d my_db -f /scripts/complex/create_top_products_in_Chiangmai_table.sql
```

### 4. Running ETL Processes
The ETL processes are implemented in Python scripts. Use the following commands to execute them:
1. **Run the first ETL process (etl_process1.py)**:
```
docker exec -it python_container python /scripts/complex/etl_process1.py
```
- This script processes data and updates the following tables:
  - user_transaction_amount
  - daily_transaction_amount
  - product_sales

2. **Run the second ETL process (etl_process2.py)**:
```
docker exec -it python_container python /scripts/complex/etl_process2.py
```
- This script processes data and updates the following tables:
  - user_location_sales
  - top_products_in_Chiangmai

### 5. Verifying the Results
Use pgAdmin or PostgreSQL queries to verify the results in each table. Below are some example queries:
1. **Check user transaction amounts**:
```
SELECT * FROM user_transaction_amount;
```

2. **Check daily transaction amounts**:
```
SELECT * FROM daily_transaction_amount;
```

3. **Check product sales**:
```
SELECT * FROM product_sales;
```

4. **Check user location sales**:
```
SELECT * FROM user_location_sales;
```

5. **Check user location sales**:
```
SELECT * FROM top_products_in_Chiangmai ORDER BY order_date, rank_num;
```

### Notes
1. **Data Duplication Prevention**:
  - Both ETL scripts (etl_process1.py and etl_process2.py) include TRUNCATE statements to clear existing data in the result tables before inserting new data. This ensures no duplication occurs when re-running the scripts.
2. **Adding New Data**:
  - If you add new CSV files to the dataset, you can simply re-run the ETL scripts to update the result tables.
3. **Error Handling**:
  - If any error occurs during the process, check the logs of the relevant service by running:
```
docker logs <container_name>
```
Replace <container_name> with postgres, pgadmin, or python_container as needed.

### Cleanup
To stop and remove all containers, networks, and volumes:
```
docker compose down -v
```

### Contact
If you have any questions, encounter issues, or need further clarification, feel free to reach out. Your feedback is always appreciated. 😊
  - Email: **k.norasit@gmail.com**