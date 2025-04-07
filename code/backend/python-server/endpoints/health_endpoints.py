"""Health check endpoints for monitoring service status"""
import time
import logging
import pymysql
from flask import jsonify

def register_health_endpoints(app, db_config):
    """
    Register health check endpoint to monitor database status
    """
    @app.route('/api/health/db', methods=['GET'])
    def db_health_check():
        """
        Database health check endpoint
        """
        healthy = False
        max_retries = 10

        for attempt in range(max_retries):
            logging.info("Attempting to access database with credentials %s", db_config)
            try:
                connection = pymysql.connect(**db_config)
                logging.info("Database connection successful!")
                healthy = True
                connection.close()
                break
            except pymysql.err.OperationalError:
                logging.warning("Attempt %(attempt)s/%(max_retries)s: Unable to connect to the database. Retrying...",
                              {"attempt": attempt + 1, "max_retries": max_retries})
                time.sleep(5)
        else:
            logging.critical("Max retries exceeded. Could not connect to the database.")

        logging.info("Status: %s", healthy)

        if healthy:
            return jsonify({"status": "healthy", "database_connection": True}), 200
        return jsonify({"status": "unhealthy", "database_connection": False}), 503
