#!/usr/bin/env python3
from connect import get_connection, run_file

def main():
    conn = get_connection()
    try:
        print("[*] Running ALL advanced queries from sql/allQ.sql ...")
        run_file(conn, "sql/allQ.sql", show_results=True)
        conn.commit()
        print("[✓] Advanced queries complete.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
