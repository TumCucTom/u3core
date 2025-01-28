#!/bin/bash
set -e

# Define the output dump file paths
DUMP_FILE="/docker-entrypoint-initdb.d/dump.sql"
LOCAL_DUMP_FILE="/host-path/initdb/dump.sql"  # Change '/host-path/' to the actual host path where you want the file

echo "Exporting MySQL database to dump files..."

# Perform the database dump
mysqldump -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --all-databases > "${DUMP_FILE}"

# Copy the dump file to a local path on the host
cp "${DUMP_FILE}" "${LOCAL_DUMP_FILE}"

echo "Database successfully exported to ${DUMP_FILE} and ${LOCAL_DUMP_FILE}"
