
PROMPT === VIEW A: ACTIVE RENTALS ===
CREATE OR REPLACE VIEW vw_active_rentals AS SELECT
    lib.username,
    c.first_name || ' ' || c.last_name AS customer_name,
    lib.movie_id,
    m.movie_name,
    lib.copy_id,
    lib.start_date,
    lib.due_date
FROM library lib, customer c, movies m
WHERE lib.returned_on IS NULL
    AND c.username = lib.username
    AND m.id = lib.movie_id;
    
PROMPT === VIEW B: Movie Inventory Status ===
CREATE OR REPLACE VIEW vw_movie_inventory_status AS SELECT
    m.id AS movie_id,
    m.movie_name,
    COUNT(inv.copy_id) AS total_copies,
    SUM(CASE WHEN inv.status = 'AVAILABLE' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN inv.status = 'RENTED' THEN 1 ELSE 0 END) AS rented,
    SUM(CASE WHEN inv.status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved
FROM movies m
LEFT JOIN inventory inv ON inv.movie_id = m.id
GROUP BY m.id, m.movie_name;

PROMPT === VIEW C: Review Stats Vs Catalog Rating ===
CREATE OR REPLACE VIEW vw_review_stats AS SELECT
    m.id AS movie_id,
    m.movie_name,
    m.avg_rating AS catalog_avg_rating,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_user_rating
FROM movies m
LEFT JOIN review r ON r.movie_id = m.id
GROUP BY m.id, m.movie_name, m.avg_rating;

PROMPT === VIEW D: Customer Rental Summary ===
CREATE OR REPLACE VIEW vw_customer_rental_summary AS SELECT
    c.username,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.balance,
    COUNT(lib.copy_id) AS total_rentals,
    SUM(CASE WHEN lib.returned_on IS NULL THEN 1 ELSE 0 END) AS active_rentals,
    MAX(lib.start_date) AS last_rental_start
FROM customer c
LEFT JOIN library lib ON lib.username = c.username
GROUP BY c.username, c.first_name, c.last_name, c.email, c.balance;

PROMPT === REVIEWS ===
CREATE OR REPLACE VIEW vw_customer_reviews AS SELECT
    c.username,
    c.first_name || ' ' || c.last_name AS customer_name,
    r.movie_id,
    m.movie_name,
    r.rating,
    r.review_text AS review,
    r.created_at AS published
FROM customer c, review r, movies m
WHERE c.username = r.username
AND m.id = r.movie_id;

EXIT;