#!/bin/bash
set -e

# Define the output dump file paths
DUMP_FILE="/docker-entrypoint-initdb.d/dump.sql"
LOCAL_DUMP_FILE="/initdb/dump.sql"

echo "Exporting MySQL database to dump files..."

# Perform the database dump
mysqldump -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --all-databases > "${DUMP_FILE}"

# Also save a local copy of the dump
cp "${DUMP_FILE}" "${LOCAL_DUMP_FILE}"

echo "Database successfully exported to ${DUMP_FILE} and ${LOCAL_DUMP_FILE}"
