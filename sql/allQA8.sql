SET PAGESIZE 200 LINESIZE 180 TRIMSPOOL ON 

PROMPT === USERS RENTING M003 ===
SELECT DISTINCT
    b.Username,
    pub.First_Name || ' ' || pub.Last_Name AS customer_name,
    mi.Movie_Name
FROM Borrow b
JOIN Movie_copy mc ON mc.Copy_ID = b.Copy_ID
JOIN Movie_information mi ON mi.Movie_ID = mc.Movie_ID
JOIN Customer_security_info sec ON sec.Username = b.Username
JOIN Customer_public_info pub ON pub.First_Name = sec.First_Name
    AND pub.Last_Name = sec.Last_Name
WHERE mc.Movie_ID = 'M003'
  AND b.Returned_On IS NULL
ORDER BY customer_name;


PROMPT === RENTED COPIES WITH QUALITIES ===
SELECT
    b.Copy_ID,
    mc.Movie_ID,
    mi.Movie_Name,
    icd.Quality,
    b.Username,
    b.Start_Date,
    b.Due_Date
FROM Borrow b
JOIN Movie_copy mc ON mc.Copy_ID = b.Copy_ID
JOIN Movie_information mi ON mi.Movie_ID = mc.Movie_ID
JOIN Inventory_Copy_Detail icd ON icd.Copy_ID = b.Copy_ID
WHERE b.Returned_On IS NULL
ORDER BY mi.Movie_Name, b.Copy_ID;


PROMPT === TOP-RATED MOVIES ===
SELECT mi.Genre, mi.Movie_Name, mi.Avg_Rating
FROM Movie_information mi
WHERE mi.Avg_Rating = (
    SELECT MAX(mi2.Avg_Rating)
    FROM Movie_information mi2
    WHERE mi2.Genre = mi.Genre
)
ORDER BY mi.Genre, mi.Avg_Rating DESC;


PROMPT === MOVIES RENTED BUT NEVER REVIEWED ===
SELECT DISTINCT mi.Movie_ID, mi.Movie_Name
FROM Movie_information mi
JOIN Movie_copy mc ON mc.Movie_ID = mi.Movie_ID
JOIN Borrow b ON b.Copy_ID = mc.Copy_ID
WHERE NOT EXISTS (
    SELECT 1 FROM Compact_Review r WHERE r.Movie_ID = mi.Movie_ID
)
ORDER BY mi.Movie_Name;


PROMPT === MOVIES STARTING WITH 'THE' ===
SELECT Movie_ID, Movie_Name
FROM Movie_information
WHERE Movie_Name LIKE 'The%'
ORDER BY Movie_Name;


PROMPT === MOVIES RELEASED 2015–2020 ===
SELECT Movie_ID, Movie_Name, Release_Date
FROM Movie_information
WHERE Release_Date BETWEEN DATE '2015-01-01' AND DATE '2020-12-31'
ORDER BY Release_Date, Movie_Name;


PROMPT === MOVIES NEVER RENTED ===
SELECT mi.Movie_ID, mi.Movie_Name
FROM Movie_information mi
WHERE mi.Movie_ID NOT IN (
    SELECT mc.Movie_ID
    FROM Movie_copy mc
    JOIN Borrow b ON b.Copy_ID = mc.Copy_ID
)
ORDER BY mi.Movie_Name;

EXIT;
