#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."

# Wait for the database to be reachable
until mysqladmin ping -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
    sleep 2
done

echo "MySQL is ready. Executing SQL dump..."

# Run the SQL dump file against the specified database
mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /usr/src/app/dump.sql || echo "SQL dump execution failed or already applied."

# Start the backend server
exec python server.py
