#!/usr/bin/env python3
from connect import get_connection, run_file

def main():
    conn = get_connection()
    try:
        print("[*] Creating tables from sql/schema.sql ...")
        run_file(conn, "sql/schemaA8.sql")
        run_file(conn, "sql/snapshotsA8.sql")
        conn.commit()
        print("[✓] Tables created successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
