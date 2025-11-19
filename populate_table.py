#!/usr/bin/env python3
from connect import get_connection, run_file

def main():
    conn = get_connection()
    try:
        print("[*] Populating tables from sql/seed.sql ...")
        run_file(conn, "sql/seed.sql")
        conn.commit()
        print("[✓] Tables populated successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
