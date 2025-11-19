#!/usr/bin/env python3
import os
import sys
import textwrap
import oracledb

# --- DB CONFIG ---
DB_USER = "a57qures"
DB_PASSWORD = "01273534"
DB_HOST = "oracle12c.cs.torontomu.ca"
DB_PORT = 1521
DB_SERVICE = "orcl12c"

# THIS LINE IS MISSING IN YOUR FILE
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    """Create and return an Oracle database connection."""
    dsn = oracledb.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)


# --- UI HELPERS ---

def pause():
    input("\nPress Enter to continue... ")

def header():
    os.system("clear" if os.name != "nt" else "cls")
    print(textwrap.dedent("""\
        =================================================================
        | Oracle All Inclusive Tool                                    |
        | Main Menu - Select Desired Operation(s):                     |
        | Make sure to run Option 1 first                              |
        | (Use Ctrl+C to stop a running step)                          |
        =================================================================
    """))


# --- SQL HELPERS ---

def run_sql(conn, sql, params=None):
    """
    Execute a SQL string and print rows (if any).
    Similar idea to the shell 'run_sql' that exits on error.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            if cur.description:  # query with results
                cols = [d[0] for d in cur.description]
                print(" | ".join(cols))
                print("-" * (len(" | ".join(cols))))
                for row in cur:
                    print(" | ".join(str(v) for v in row))
    except oracledb.Error as e:
        print("ERROR while running SQL:")
        print(e)
        sys.exit(1)

def run_file(conn, relative_path, show_results=False):
    """
    Execute all SQL statements in a .sql file.

    - Strips common SQL*Plus-only commands (WHENEVER, SET, SPOOL, PROMPT, @file, CONNECT, /, EXIT)
    - Splits remaining content on ';'
    - Prints the exact statement if Oracle throws an error
    """
    path = relative_path
    if not os.path.isabs(path):
        path = os.path.join(SCRIPT_DIR, relative_path)

    if not os.path.exists(path):
        print(f"SQL file not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned_lines = []
    for line in content.splitlines():
        stripped = line.strip()
        upper = stripped.upper()

        # Skip blank lines
        if not stripped:
            continue

        # Skip common SQL*Plus commands
        if (
            upper.startswith("WHENEVER ")
            or upper.startswith("SET ")
            or upper.startswith("SPOOL ")
            or upper.startswith("PROMPT")
            or upper.startswith("COLUMN ")
            or upper.startswith("TTITLE ")
            or upper.startswith("BTITLE ")
            or upper.startswith("CONNECT ")
            or upper.startswith("CONN ")
            or stripped.startswith("@")   # @otherfile.sql
            or upper == "EXIT"
            or upper == "/"               # sqlplus block terminator
        ):
            continue

        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    statements = [s.strip() for s in cleaned.split(";") if s.strip()]

    try:
        with conn.cursor() as cur:
            for idx, stmt in enumerate(statements, start=1):
                # Skip stray EXIT statements that came from sqlplus-style scripts
                if stmt.strip().upper() == "EXIT":
                    # Optional: print a note
                    # print(f"[info] Skipping EXIT in statement #{idx}")
                    continue

                try:
                    # print(f"\n[DEBUG] Statement #{idx}:\n{stmt}\n")  # for debugging if needed
                    cur.execute(stmt)
                    if show_results and cur.description:
                        cols = [d[0] for d in cur.description]
                        print(" | ".join(cols))
                        print("-" * (len(" | ".join(cols))))
                        for row in cur:
                            print(" | ".join(str(v) for v in row))
                except oracledb.Error as e:
                    print(f"\nERROR while running SQL file, in statement #{idx}:")
                    print("------------------------------------------------------")
                    print(stmt)
                    print("------------------------------------------------------")
                    print("Oracle error:", e)
                    sys.exit(1)


        conn.commit()

    except oracledb.Error as e:
        print("ERROR while running SQL file:")
        print(e)
        sys.exit(1)


# --- MAIN ---

def main():
    header()
    print("Testing connection...")

    try:
        conn = get_connection()
    except oracledb.Error as e:
        print("Failed to connect to Oracle:")
        print(e)
        sys.exit(1)

    # Quick test query (same as your shell script)
    run_sql(conn, "SELECT USER AS connected_as FROM dual")

    # Example: if you later want a menu, you can add it here.
    # For now we just pause and exit.
    pause()
    conn.close()


if __name__ == "__main__":
    main()
