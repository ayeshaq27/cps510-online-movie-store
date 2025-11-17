#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "${SCRIPT_DIR}/conn.sh"
sqlplus -s -L "${ORA_CONNECT}" @"${SCRIPT_DIR}/sql/seed.sql"