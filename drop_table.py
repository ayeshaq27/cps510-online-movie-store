#!/usr/bin/env python3
import oracledb
from connect import get_connection

TABLES = [
    "Review",
    "Library",
    "Inventory",
    "Customer",
    "Movies",
    "Customer_Service",
    "Content_Manager",
    "Developer",
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
