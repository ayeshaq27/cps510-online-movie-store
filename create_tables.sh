#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "${SCRIPT_DIR}/conn.sh"
sqlplus -s -L "${ORA_CONNECT}" @"${SCRIPT_DIR}/sql/schema.sql"
# filepath: c:\workspace\CPS510\create_tables.sh