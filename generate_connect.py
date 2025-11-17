import getpass

host = "oracle12c.cs.torontomu.ca"
port = "1521"
service_name = "orcl12c"

username = input("Enter Oracle username: ")
password = getpass.getpass("Enter Oracle password: ")

connect_str = (
    f"{username}/{password}"
    f"@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))"
    f"(CONNECT_DATA=(SERVICE_NAME={service_name})))"
)

# print only the connect string so conn.sh can capture it
print(connect_str)