#!/bin/bash
set -e

# Define the output dump file path
DUMP_FILE="/docker-entrypoint-initdb.d/dump.sql"

echo "Exporting MySQL database to dump file..."

# Perform the database dump
mysqldump -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --all-databases > "${DUMP_FILE}"

echo "Database successfully exported to ${DUMP_FILE}"
