SET PAGESIZE 200
SET LINESIZE 180
SET TRIMSPOOL ON

COLUMN customer_name   HEADING 'CUSTOMER'       FORMAT A22
COLUMN movie_name      HEADING 'MOVIE'          FORMAT A28
COLUMN copy_id         HEADING 'COPY'           FORMAT A8
COLUMN start_date      HEADING 'START'          FORMAT A12
COLUMN due_date        HEADING 'DUE'            FORMAT A12
COLUMN available       HEADING 'AVAILABLE'
COLUMN rented          HEADING 'RENTED'
COLUMN reserved        HEADING 'RESVD'

PROMPT === ACTIVE RENTALS (Borrow + Movie_information + Movie_copy) ===
SELECT
    username,
    customer_name,
    movie_id,
    movie_name,
    copy_id,
    start_date,
    due_date
FROM vw_active_rentals
ORDER BY due_date, movie_name;

PROMPT === MOVIE INVENTORY STATUS (Movie_copy + Inventory_Copy_Detail) ===
SELECT
    movie_id,
    movie_name,
    total_copies,
    available,
    rented,
    reserved
FROM vw_movie_inventory_status
ORDER BY movie_name;

PROMPT === REVIEW STATS (Compact_Review + Movie_information) ===
SELECT
    movie_id,
    movie_name,
    catalog_avg_rating,
    review_count,
    avg_user_rating
FROM vw_review_stats
ORDER BY review_count DESC, movie_name;

PROMPT === CUSTOMER REVIEWS (Compact_Review + Customer_security_info + public info) ===
SELECT
    username,
    customer_name,
    movie_id,
    movie_name,
    rating,
    review,
    published
FROM vw_customer_reviews
ORDER BY published DESC, movie_name;

PROMPT === CUSTOMER RENTAL SUMMARY (Borrow + Customer tables) ===
SELECT
    username,
    customer_name,
    email,
    balance,
    total_rentals,
    active_rentals,
    last_rental_start
FROM vw_customer_rental_summary
ORDER BY active_rentals DESC, total_rentals DESC, customer_name;

EXIT;
