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
#!/bin/sh

# If ORA_CONNECT already set (exported by parent), don't prompt again.
if [ -n "${ORA_CONNECT:-}" ]; then
  return 0 2>/dev/null || exit 0
fi

host="oracle12c.cs.torontomu.ca"
port="1521"
service_name="orcl12c"

# prefer python3 then python; determine path to generate_connect.py if caller set SCRIPT_DIR
if command -v python3 >/dev/null 2>&1; then
  PY_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PY_BIN=python
else
  PY_BIN=""
fi

if [ -n "${PY_BIN}" ]; then
  if [ -n "${SCRIPT_DIR:-}" ] && [ -f "${SCRIPT_DIR}/generate_connect.py" ]; then
    PY_SCRIPT="${SCRIPT_DIR}/generate_connect.py"
  elif [ -f "./generate_connect.py" ]; then
    PY_SCRIPT="./generate_connect.py"
  else
    PY_SCRIPT=""
  fi

  if [ -n "${PY_SCRIPT}" ]; then
    # invoke python script and capture stdout as the connect string
    ORA_CONNECT="$("$PY_BIN" "${PY_SCRIPT}" 2>/dev/null || echo "")"
    if [ -n "${ORA_CONNECT}" ]; then
      export ORA_CONNECT
      return 0 2>/dev/null || exit 0
    fi
  fi
fi

# Fallback: interactive shell prompt (keeps original behavior)
printf "Enter Oracle username: "
read -r ORA_USER
printf "Enter Oracle password: "
stty -echo; read -r ORA_PASS; stty echo; printf "\n"

ORA_CONNECT="${ORA_USER}/${ORA_PASS}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=${host})(PORT=${port}))(CONNECT_DATA=(SERVICE_NAME=${service_name})))"
export ORA_CONNECT
export ORA_CONNECT