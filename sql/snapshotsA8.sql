SET PAGESIZE 200
SET LINESIZE 180
SET TRIMSPOOL ON

COLUMN customer_name   HEADING 'CUSTOMER' FORMAT A22
COLUMN movie_name      HEADING 'MOVIE'    FORMAT A28
COLUMN copy_id         HEADING 'COPY'     FORMAT A8
COLUMN start_date      HEADING 'START'    FORMAT A12
COLUMN due_date        HEADING 'DUE'      FORMAT A12
COLUMN available       HEADING 'AVAILABLE'
COLUMN rented          HEADING 'RENTED'
COLUMN reserved        HEADING 'RESVD'

PROMPT === ACTIVE RENTALS ===
SELECT * FROM vw_active_rentals
ORDER BY due_date, movie_name;


PROMPT === MOVIE INVENTORY STATUS ===
SELECT * FROM vw_movie_inventory_status
ORDER BY movie_name;


PROMPT === REVIEW STATS ===
SELECT * FROM vw_review_stats
ORDER BY review_count DESC, movie_name;


PROMPT === REVIEWS ===
SELECT * FROM vw_customer_reviews
ORDER BY published DESC, movie_name;


PROMPT === CUSTOMER RENTAL SUMMARY ===
SELECT * FROM vw_customer_rental_summary
ORDER BY active_rentals DESC, total_rentals DESC, customer_name;

EXIT;
