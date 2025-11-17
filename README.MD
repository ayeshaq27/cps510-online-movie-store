Run this first:
dos2unix conn.sh menu_app.sh drop_tables.sh create_tables.sh populate_tables.sh sql/*.sql || true

Then this:
chmod +x menu_app.sh drop_tables.sh create_tables.sh populate_tables.sh

Then last:

./menu_app.sh
