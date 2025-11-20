#!/usr/bin/env python3
import sys
from connect import header, pause, get_connection, run_sql
import drop_table
import drop_table_A8
import create_table
import populate_table
import queries
import snapshots      # <-- add this
import create_table_A8


def main():
    # quick connection test
    print("Testing connection...")
    try:
        conn = get_connection()
    except Exception as e:
        print("Failed to connect to Oracle:")
        print(e)
        sys.exit(1)

    run_sql(conn, "SELECT USER AS connected_as FROM dual")
    conn.close()
    pause()

    while True:
        header()
        print("  1) Drop Tables")
        print("  2) Create Tables")
        print("  3) Populate Tables")
        print("  4) Snapshots (from views)")
        print("  5) Run ALL Advanced Queries (allQ.sql)\n")
        print("  6) Run ALL Advanced Queries BNF\n")
        print("  E) End/Exit\n")
        choice = input("Choose: ").strip()

        if choice == "1":
            drop_table.main()
            pause()

        elif choice == "2":
            create_table.main()
            pause()

        elif choice == "3":
            populate_table.main()
            pause()

        elif choice == "4":
            # If you later make a snapshots.py that runs a5_views + snapshots.sql, call it here
            snapshots.main()
            pause()

        elif choice == "5":
            queries.main()
            pause()
        
        elif choice == "6":
            drop_table_A8.main()
            create_table_A8.main()
            pause()

        elif choice in ("E", "e", "Q", "q", "0"):
            print("Bye!")
            sys.exit(0)

        else:
            print("Invalid option.")
            pause()

if __name__ == "__main__":
    main()
