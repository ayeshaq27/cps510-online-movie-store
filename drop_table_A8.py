#!/usr/bin/env python3
import oracledb
from connect import get_connection

# Drop child tables first, then parent tables
TABLES = [
    # Child tables
    "Borrow",                      # FK → Movie_copy, Customer_security_info
    "Inventory_Copy_Detail",       # FK → Movie_copy
    "Compact_Review",              # FK → Movie_information, Customer_security_info
    "Shift_info_customer_service", # FK → Employee_info_customer_service
    "CM_movie_to_change",          # FK → Employee_info_CM, Movie_information
    "Developer_speciality",        # FK → Developer_main (Email, Github)

    # Mid-level / parent tables
    "Movie_copy",                  # FK → Movie_information
    "Customer_security_info",
    "Customer_public_info",
    "Employee_info_customer_service",
    "Employee_info_CM",
    "Developer_main",
    "Movie_information",
]

def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for t in TABLES:
                plsql = f"""
                BEGIN
                    EXECUTE IMMEDIATE 'DROP TABLE {t} PURGE';
                EXCEPTION
                    WHEN OTHERS THEN NULL;
                END;
                """
                try:
                    cur.execute(plsql)
                    print(f"Dropped table (if existed): {t}")
                except oracledb.Error as e:
                    # Should be swallowed by PL/SQL, but just in case:
                    print(f"Error dropping {t}: {e}")
        conn.commit()
        print("[✓] Drop complete.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
