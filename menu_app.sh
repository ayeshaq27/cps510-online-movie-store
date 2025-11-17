#!/bin/sh
# menu_app.sh — hardcoded connection via conn.sh

set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# load hardcoded connect string
# shellcheck disable=SC1090
. "${SCRIPT_DIR}/conn.sh"

pause() { printf "\nPress Enter to continue... "; read -r _; }
header() {
  clear
  cat <<'TXT'
=================================================================
| Oracle All Inclusive Tool                                    |
| Main Menu - Select Desired Operation(s):                     |
| Make sure to run Option 1 first                              |
| (Use Ctrl+C to stop a running step)                          |
=================================================================
TXT
}

# helpers
run_file() {
  sql_file="$1"
  sqlplus -s -L "${ORA_CONNECT}" @"$sql_file"
}
run_sql() {
  body="$1"
  TMP_SQL="$(mktemp)"
  {
    printf "WHENEVER SQLERROR EXIT SQL.SQLCODE\n"
    printf "%s\n" "$body"
    printf "EXIT;\n"
  } > "$TMP_SQL"
  sqlplus -s -L "${ORA_CONNECT}" @"$TMP_SQL"
  rm -f "$TMP_SQL"
}


# quick connect test
echo "Testing connection..."
run_sql "SELECT user AS connected_as FROM dual;"

# menu
while : ; do
  header
  printf "  1) Drop Tables\n"
  printf "  2) Create Tables\n"
  printf "  3) Populate Tables\n"
  printf "  4) Snapshots (from views)\n"
  printf "  5) Run ALL Advanced Queries (allQ.sql)\n\n"
  printf "  E) End/Exit\n\n"
  printf "Choose: "
  read -r CHOICE

  case "$CHOICE" in
    
    1)
      echo "[*] Dropping tables ..."
      sh "${SCRIPT_DIR}/drop_tables.sh"
      echo "[✓] Drop complete."; pause ;;
    2)
      echo "[*] Creating tables ..."
      sh "${SCRIPT_DIR}/create_tables.sh"
      echo "[✓] Create complete."; pause ;;
    3)
      echo "[*] Populating tables ..."
      sh "${SCRIPT_DIR}/populate_tables.sh"
      echo "[✓] Populate complete."; pause ;;
    4)
      echo "[*] Creating/refreshing views then running snapshots ..."
      run_file "${SCRIPT_DIR}/sql/a5_views.sql"
      run_file "${SCRIPT_DIR}/sql/snapshots.sql"
      echo "[✓] Snapshots done."; pause ;;
    5)
      echo "[*] Running ALL advanced queries ..."
      run_file "${SCRIPT_DIR}/sql/allQ.sql"
      echo "[✓] Advanced queries complete."; pause ;;
    E|e|Q|q|0) echo "Bye!"; exit 0 ;;
    *) echo "Invalid option."; sleep 1 ;;
  esac
done
