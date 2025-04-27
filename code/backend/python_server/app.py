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
from database import initialise_database
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
from endpoints.health_endpoints import register_health_endpoints

def create_app():
    """Create and configure the Flask app"""
    # Load environment variables
    load_dotenv()
    postmark_api = os.getenv("POSTMARK_API")

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
    _ = load_config()  # Config loaded but not used directly here

    flask_app = Flask(__name__)
    CORS(flask_app)  # Enable CORS for all routes

    # Database Configuration
    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "3306"))
    }

    # Try connecting to the database with retries
    max_retries = 10
    db_connection = None
    for attempt in range(max_retries):
        try:
            db_connection = pymysql.connect(**db_config)
            logging.info("Database connection successful!")
            break
        except pymysql.err.OperationalError:
            logging.warning(
                "Attempt %(attempt)s/%(max_retries)s: Unable to connect to database. Retrying...",
                {"attempt": attempt + 1, "max_retries": max_retries}
            )
            time.sleep(5)
    else:
        logging.critical("Max retries exceeded. Could not connect to the database.")

    # Initialize database tables
    initialise_database(db_config)

    # Register endpoints
    register_camera_endpoints(flask_app, db_config, fire_detection_processes, run_fire_detection)
    register_site_endpoints(flask_app, db_config, fire_detection_processes)
    register_hazard_endpoints(flask_app, db_config)
    register_analytics_endpoints(flask_app, db_config)
    register_user_endpoints(flask_app, db_config, postmark_api)
    register_health_endpoints(flask_app, db_config)

    return flask_app, db_connection

if __name__ == '__main__':
    app, connection = create_app()
    if connection:
        start_fire_detection_for_all_cameras(
            connection,
            fire_detection_processes,
            run_fire_detection
        )
    app.run(host='0.0.0.0', port=3000, debug=True)
