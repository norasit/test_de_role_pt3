CREATE TABLE IF NOT EXISTS transaction (
    order_id SERIAL PRIMARY KEY,  -- ลำดับคำสั่งซื้อ (primary key)
    user_id INT,                  -- รหัสผู้ใช้งาน
    product_id INT,               -- รหัสสินค้า
    quantity INT,                 -- จำนวนสินค้า
    amount DECIMAL(10, 2),        -- ยอดเงิน
    order_date DATE               -- วันที่คำสั่งซื้อ
);
