"""Utility functions for API endpoints"""
import logging
import pymysql
from flask import jsonify
from database import get_db_connection

def get_count_from_table(table_name, db_config, condition=None, condition_values=None):
    """
    Fetch count from the specified table.
    """
    try:
        conn = get_db_connection(db_config)
        with conn.cursor() as cursor:
            # Check if table exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                AND table_name = %s;
            """, (table_name,))
            table_exists = cursor.fetchone()[0] > 0

            if not table_exists:
                logging.info("Table '%s' does not exist. Returning 0.", table_name)
                return jsonify(0), 200  # Return 0 count if table does not exist

            # Build query with an optional condition
            query = f"SELECT COUNT(*) AS count FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"

            cursor.execute(query, condition_values or ())
            row_count = cursor.fetchone()[0]

        return jsonify(row_count), 200

    except (pymysql.Error, ValueError) as error:
        logging.error(
            "Error fetching count from %(table)s: %(error)s",
            {"table": table_name, "error": error}
        )
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn:
            conn.close()
