-- โหลดข้อมูลจาก user_info.csv
COPY user_info (user_id, age, gender, location)
FROM '/data/user_info.csv'
DELIMITER ','
CSV HEADER;