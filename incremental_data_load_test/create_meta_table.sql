CREATE TABLE IF NOT EXISTS meta_data (
    file_name TEXT PRIMARY KEY,   -- ชื่อไฟล์ CSV
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- เวลาที่โหลดไฟล์
);
