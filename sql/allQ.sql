-- sql/allQ.sql
SET PAGESIZE 200 LINESIZE 180 TRIMSPOOL ON 
PROMPT === USERS RENTING M003 ===
SELECT DISTINCT 
  lib.username, 
  c.username || ' '|| c.last_name AS customer_name,
  m.movie_name
FROM library lib, customer c, movies m
WHERE c.username = lib.username
  AND m.id       = lib.movie_id
  AND lib.movie_id = 'M003'
  AND lib.returned_on IS NULL
ORDER BY customer_name;

PROMPT === RENTED COPIES WITH QUALITIES ===
SELECT
  lib.copy_id,
  lib.movie_id,
  m.movie_name,
  inv.quality,
  lib.username,
  lib.start_date,
  lib.due_date
FROM library lib, movies m, inventory inv
WHERE inv.copy_id = lib.copy_id
  AND m.id        = lib.movie_id
  AND lib.returned_on IS NULL
ORDER BY m.movie_name, lib.copy_id;

PROMPT === TOP-RATED MOVIES ===
SELECT m.genre, m.movie_name, m.avg_rating
FROM movies m
WHERE m.avg_rating = (
  SELECT MAX(m2.avg_rating) 
  FROM movies m2 
  WHERE m2.genre = m.genre
)
ORDER BY m.genre, m.avg_rating DESC;

PROMPT === MOVIE RENTALS WITHOUT CUSTOMER REVIEWS ===
SELECT DISTINCT m.id AS movie_id, m.movie_name
FROM movies m, library lib
WHERE lib.movie_id = m.id
  AND NOT EXISTS (SELECT 1 FROM review r WHERE r.movie_id = m.id)
ORDER BY m.movie_name;

PROMPT === Movies starting with THE ===
SELECT m.id, m.movie_name
FROM movies m
WHERE m.movie_name LIKE 'The%'
ORDER BY m.movie_name;

PROMPT === Movies released between 2015 to 2020 ===
SELECT m.id, m.movie_name, m.release_date
FROM movies m
WHERE m.release_date BETWEEN DATE '2015-01-01' AND DATE '2020-12-31'
ORDER BY m.release_date, m.movie_name;

PROMPT === Movies never rented ===
SELECT m.id, m.movie_name
FROM movies m
WHERE m.id NOT IN (SELECT lib.movie_id FROM library lib)
ORDER BY m.movie_name;
EXIT;