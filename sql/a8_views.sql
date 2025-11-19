PROMPT === VIEW A: ACTIVE RENTALS ===
CREATE OR REPLACE VIEW vw_active_rentals AS
SELECT
    b.username,
    pub.first_name || ' ' || pub.last_name AS customer_name,
    mc.Movie_ID,
    mi.Movie_Name,
    b.Copy_ID,
    b.Start_Date,
    b.Due_Date
FROM Borrow b
JOIN Movie_copy mc ON mc.Copy_ID = b.Copy_ID
JOIN Movie_information mi ON mi.Movie_ID = mc.Movie_ID
JOIN Customer_security_info sec ON sec.Username = b.Username
JOIN Customer_public_info pub ON pub.First_Name = sec.First_Name
    AND pub.Last_Name = sec.Last_Name
WHERE b.Returned_On IS NULL;


PROMPT === VIEW B: MOVIE INVENTORY STATUS ===
CREATE OR REPLACE VIEW vw_movie_inventory_status AS
SELECT
    mi.Movie_ID,
    mi.Movie_Name,
    COUNT(mc.Copy_ID) AS total_copies,
    SUM(CASE WHEN icd.Status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN icd.Status = 'RENTED' THEN 1 ELSE 0 END) AS rented,
    SUM(CASE WHEN icd.Status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved
FROM Movie_information mi
LEFT JOIN Movie_copy mc ON mc.Movie_ID = mi.Movie_ID
LEFT JOIN Inventory_Copy_Detail icd ON icd.Copy_ID = mc.Copy_ID
GROUP BY mi.Movie_ID, mi.Movie_Name;


PROMPT === VIEW C: REVIEW STATS VS CATALOG RATING ===
CREATE OR REPLACE VIEW vw_review_stats AS
SELECT
    mi.Movie_ID,
    mi.Movie_Name,
    mi.Avg_Rating AS catalog_avg_rating,
    COUNT(r.Review_ID) AS review_count,
    ROUND(AVG(r.Rating), 2) AS avg_user_rating
FROM Movie_information mi
LEFT JOIN Compact_Review r ON r.Movie_ID = mi.Movie_ID
GROUP BY mi.Movie_ID, mi.Movie_Name, mi.Avg_Rating;


PROMPT === VIEW D: CUSTOMER RENTAL SUMMARY ===
CREATE OR REPLACE VIEW vw_customer_rental_summary AS
SELECT
    sec.Username,
    pub.First_Name || ' ' || pub.Last_Name AS customer_name,
    pub.Email,
    sec.Balance,
    COUNT(b.Copy_ID) AS total_rentals,
    SUM(CASE WHEN b.Returned_On IS NULL THEN 1 ELSE 0 END) AS active_rentals,
    MAX(b.Start_Date) AS last_rental_start
FROM Customer_security_info sec
JOIN Customer_public_info pub ON pub.First_Name = sec.First_Name
    AND pub.Last_Name = sec.Last_Name
LEFT JOIN Borrow b ON b.Username = sec.Username
GROUP BY sec.Username, pub.First_Name, pub.Last_Name, pub.Email, sec.Balance;


PROMPT === REVIEWS ===
CREATE OR REPLACE VIEW vw_customer_reviews AS
SELECT
    sec.Username,
    pub.First_Name || ' ' || pub.Last_Name AS customer_name,
    r.Movie_ID,
    mi.Movie_Name,
    r.Rating,
    r.Review_Text AS review,
    r.Created_At AS published
FROM Compact_Review r
JOIN Customer_security_info sec ON sec.Username = r.Username
JOIN Customer_public_info pub ON pub.First_Name = sec.First_Name
    AND pub.Last_Name = sec.Last_Name
JOIN Movie_information mi ON mi.Movie_ID = r.Movie_ID;

EXIT;
