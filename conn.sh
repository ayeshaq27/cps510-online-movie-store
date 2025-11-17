#!/bin/sh

# If ORA_CONNECT already set (exported by parent), don't prompt again.
if [ -n "${ORA_CONNECT:-}" ]; then
  # return if sourced, otherwise exit
  return 0 2>/dev/null || exit 0
fi

host="oracle12c.cs.torontomu.ca"
port="1521"
service_name="orcl12c"

printf "Enter Oracle username: "
read -r ORA_USER
printf "Enter Oracle password: "
stty -echo; read -r ORA_PASS; stty echo; printf "\n"

ORA_CONNECT="${ORA_USER}/${ORA_PASS}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=${host})(PORT=${port}))(CONNECT_DATA=(SERVICE_NAME=${service_name})))"

export ORA_CONNECT