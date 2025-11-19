#!/usr/bin/env python3
from connect import get_connection
import oracledb

def print_table(conn, table_name):
    print(f"\n==================== {table_name} ====================")
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()

            # Column names
            cols = [d[0] for d in cur.description]
            print(" | ".join(cols))
            print("-" * (len(" | ".join(cols))))

            for r in rows:
                print(" | ".join(str(x) for x in r))

    except oracledb.Error as e:
        print(f"[Error reading {table_name}]: {e}")
    print()  # spacing


def main():
    conn = get_connection()
    try:
        # Optionally refresh views
        print("[*] Refreshing views from sql/a5_views.sql ...")
        from connect import run_file
        run_file(conn, "sql/a5_views.sql")

        print("[*] Fetching list of all user tables...")

        with conn.cursor() as cur:
            cur.execute("SELECT table_name FROM user_tables ORDER BY table_name")
            tables = [row[0] for row in cur.fetchall()]

        print(f"Found {len(tables)} tables.")

        # Print each table
        for t in tables:
            print_table(conn, t)

        print("[✓] Printed all tables.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
