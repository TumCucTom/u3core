"""Main application entry point"""
import os
import logging
import sys
import time
import pymysql
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Import modules
from config import load_config
from database import get_db_connection, initialise_database
from fire_detection import (
    fire_detection_processes,
    run_fire_detection,
    start_fire_detection_for_all_cameras
)
from endpoints.camera_endpoints import register_camera_endpoints
from endpoints.site_endpoints import register_site_endpoints
from endpoints.hazard_endpoints import register_hazard_endpoints
from endpoints.analytics_endpoints import register_analytics_endpoints
from endpoints.user_endpoints import register_user_endpoints

def create_app():
    """Create and configure the Flask app"""
    # Load environment variables
    load_dotenv()
    POSTMARK_API = os.getenv("POSTMARK_API")

    # Load environment variables from ../../../.env
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
    load_dotenv(dotenv_path)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Load configuration from JSON
    config = load_config()

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Database Configuration
    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "3306"))
    }

    # Try connecting to the database with retries
    MAX_RETRIES = 10
    connection = None
    for attempt in range(MAX_RETRIES):
        try:
            connection = pymysql.connect(**db_config)
            logging.info("Database connection successful!")
            break
        except pymysql.err.OperationalError as e:
            logging.warning(f"Attempt {attempt + 1}/{MAX_RETRIES}: Unable to connect to the database. Retrying...")
            time.sleep(5)
    else:
        logging.critical("Max retries exceeded. Could not connect to the database.")

    # Initialize database tables
    initialise_database(db_config)

    # Register endpoints
    register_camera_endpoints(app, db_config, fire_detection_processes, run_fire_detection)
    register_site_endpoints(app, db_config, fire_detection_processes)
    register_hazard_endpoints(app, db_config)
    register_analytics_endpoints(app, db_config)
    register_user_endpoints(app, db_config, POSTMARK_API)

    return app, connection

if __name__ == '__main__':
    app, connection = create_app()
    if connection:
        start_fire_detection_for_all_cameras(
            connection,
            fire_detection_processes,
            run_fire_detection
        )
    app.run(host='0.0.0.0', port=3000, debug=True)