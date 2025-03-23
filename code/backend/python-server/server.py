"""Backend python server for api endpoints and fire detection"""
# pylint: disable=line-too-long
# pylint: disable=broad-except
# pylint: disable=logging-fstring-interpolation
# pylint: disable=c-extension-no-member
# pylint: disable=too-many-locals

import os
import random
import string
import secrets
from io import BytesIO
import multiprocessing
import json
import time
import logging
import sys
import datetime
import pymysql
import pycurl
import requests
from fire_detection_script import process_rtsp_stream_with_url
from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from dotenv import load_dotenv


load_dotenv()
POSTMARK_API = os.getenv("POSTMARK_API")

# Load configuration from JSON
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Alert message
ALERT_MESSAGE = "Abnormal detected"

# Load environment variables from ../../../.env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Database Configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

MAX_RETRIES = 10
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

def get_db_connection():
    """Return a fresh connection to the database."""
    return pymysql.connect(**db_config)

# Auto fire detection startup

# Dictionary to track running fire detection processes
fire_detection_processes = {}

def run_fire_detection(rtsp_url):
    """Run the fire detection script for a given RTSP URL."""
    logging.info("Running fire detection on {rtsp_url}")
    process_rtsp_stream_with_url(rtsp_url)

def start_fire_detection_for_all_cameras():
    """
    Fetch all cameras from the database and start fire detection concurrently.
    Ensures each RTSP stream is monitored independently.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT rtsp_url FROM Cameras")
            cameras = cursor.fetchall()
        for (rtsp_url,) in cameras:
            if rtsp_url not in fire_detection_processes:  # Avoid duplicate processes
                process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
                process.start()
                fire_detection_processes[rtsp_url] = process
                logging.info(f"Started fire detection for: {rtsp_url}")
        logging.info("Started fire detection for all cameras")
    except Exception as e:
        print(f"Error starting fire detection processes: {e}")

# API endpoints

@app.route('/api/add-camera', methods=['POST'])
def add_camera():
    """
    Adds a new RTSP camera to the database and starts fire detection for it.
    Converts tcp:// to rtsp:// if necessary and updates existing records.
    """
    data = request.json
    name = data.get('name')
    rtsp_url = data.get('rtsp_url')

    if not all([name, rtsp_url]):
        return jsonify({"error": "Name and RTSP URL are required"}), 400

    # Convert tcp:// to rtsp://
    if rtsp_url.startswith("tcp://"):
        rtsp_url = "rtsp://" + rtsp_url[6:]

    try:
        # Create the Cameras table if it doesn't exist
        conn = get_db_connection()
        with conn.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Cameras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                rtsp_url TEXT
                site_id INT,
                FOREIGN KEY (site_id) REFERENCES Sites(id)
            );
            """
            cursor.execute(create_table_query)

            # Update any existing entries that start with tcp://
            update_query = """
            UPDATE Cameras
            SET rtsp_url = CONCAT('rtsp://', SUBSTRING(rtsp_url, 7))
            WHERE rtsp_url LIKE 'tcp://%';
            """
            cursor.execute(update_query)

            # Insert the new camera data
            cursor.execute(
                "INSERT INTO Cameras (name, rtsp_url) VALUES (%s, %s)",
                (name, rtsp_url)
            )
        conn.commit()

        # Start fire detection for the new camera
        if rtsp_url not in fire_detection_processes:
            process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
            process.start()
            fire_detection_processes[rtsp_url] = process
            print(f"Started fire detection for new camera: {rtsp_url}")
        return jsonify(
            {"message": "Camera added, TCP URLs updated, and fire detection started!"}), 201

    except Exception as e:
        print(f"Error adding camera: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/add-site', methods=['POST'])
def add_site():
    """
    Adds a new site with name, latitude, and longitude to the database.
    """
    data = request.json
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([name, latitude, longitude]):
        return jsonify({"error": "Name, latitude, and longitude are required"}), 400

    try:
        conn = get_db_connection()
        # Create the Sites table if it doesn't exist
        with conn.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Sites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                latitude VARCHAR(50),
                longitude VARCHAR(50)
            );
            """
            cursor.execute(create_table_query)

            # Insert the site data
            cursor.execute(
                "INSERT INTO Sites (name, latitude, longitude) VALUES (%s, %s, %s)",
                (name, latitude, longitude)
            )
        conn.commit()
        return jsonify({"message": "Site added successfully!"}), 201
    except Exception as e:
        print(f"Error adding site: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/sites', methods=['GET'])
def fetch_sites():
    """
    Fetches all sites and their associated cameras.
    """
    try:
        # Fetch all sites
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM Sites")
            sites = cursor.fetchall()

            # Fetch cameras for each site
            result = []
            for site in sites:
                site_id, name = site
                cursor.execute(
                    "SELECT id, name FROM Cameras WHERE site_id = %s", (site_id,))
                cameras = [{"id": cam_id, "name": cam_name} for cam_id, cam_name in cursor.fetchall()]
                result.append({"id": site_id, "name": name, "cameras": cameras})

        return jsonify({"sites": result}), 200
    except Exception as e:
        print(f"Error fetching sites: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/add-hazard', methods=['POST'])
def add_hazard():
    """
    Adds a new hazard log, ensuring proper tracking based on time, camera, and hazard type.
    """
    data = request.json
    timestamp = data.get('timestamp')
    hazard_type = data.get('type')
    rtsp_url = data.get('cameraAddress')   # Assuming cameraAddress holds rtsp_url

    if not all([rtsp_url, timestamp, hazard_type]):
        return jsonify({"error": "Camera address, time, and hazard type are required"}), 400

    try:
        # Fetch camera name from the Cameras table
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM Cameras WHERE rtsp_url = %s", (rtsp_url,))
            camera_result = cursor.fetchone()

            if not camera_result:
                return jsonify({"error": "Camera not found"}), 404

            camera_name = camera_result[0]

            # Extract date and hour from timestamp
            timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            hour_time = timestamp_obj.strftime("%Y-%m-%d %H")  # Date and hour only

            # Create the Logs table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cameraIP VARCHAR(255),
                cameraName VARCHAR(255),
                hourTime VARCHAR(50),
                hazardType VARCHAR(50),
                number INT DEFAULT 1,
                falsePositive BOOLEAN DEFAULT FALSE
            );
            """
            cursor.execute(create_table_query)

 # Check if an entry exists for the same cameraIP, hazardType, and hourTime
            cursor.execute("""
                SELECT id, number FROM Logs
                WHERE cameraIP = %s AND hazardType = %s AND hourTime = %s
            """, (rtsp_url, hazard_type, hour_time))

            existing_entry = cursor.fetchone()

            if existing_entry:
                log_id, current_number = existing_entry
                new_number = current_number + 1
                false_positive = 1 <= new_number <= 9
                # Update the existing entry
                cursor.execute("""
                    UPDATE Logs
                    SET number = %s, falsePositive = %s
                    WHERE id = %s
                """, (new_number, false_positive, log_id))
            else:
                # Insert a new log entry
                cursor.execute("""
                    INSERT INTO Logs (cameraIP, cameraName, hourTime, hazardType, number, falsePositive)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (rtsp_url, camera_name, hour_time, hazard_type, 1, True))

        conn.commit()
        return jsonify({"message": "Log added successfully!"}), 201

    except Exception as e:
        print(f"Error adding log: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/get-logs', methods=['GET'])
def get_logs():
    """
    Fetch all hazard log entries from the logs table and return them in a format
    compatible with the front end
    """
    try:
        # Retrieve all log entries sorted by most recent first
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, cameraIP, cameraName, hourTime, hazardType, number, falsePositive
                FROM Logs
                ORDER BY id DESC
            """)
            rows = cursor.fetchall()

            # Transform rows into a list of dictionaries
            data = []
            for row in rows:
                log_id, camera_ip, camera_name, hour_time, hazard_type, number, false_positive = row

                data.append({
                    "id": log_id,
                    "cameraName": camera_name,
                    "cameraAddress": camera_ip,
                    "timestamp": hour_time,
                    "faultType": hazard_type,
                    "numberOfHazards": number,
                    "falsePositives": "Yes" if false_positive else "No"
                })

        return jsonify(data), 200

    except Exception as e:
        print("Error retrieving logs:", e)
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        conn.close()

def get_count_from_table(table_name, condition=None, condition_values=None):
    """
    Fetch hazard/cameraas/site count from the specified table.
    """
    try:
        conn = get_db_connection()
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
                print(f"Table '{table_name}' does not exist. Returning 0.")
                return jsonify(0), 200  # Return 0 count if table does not exist

            # Build query with an optional condition (falsePositive = 0)
            query = f"SELECT COUNT(*) AS count FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"

            cursor.execute(query, condition_values or ())
            row_count = cursor.fetchone()[0]

        conn.commit()
        return jsonify(row_count), 200

    except pymysql.MySQLError as e:
        print(f"MySQL error while fetching {table_name} count:", e)
        return jsonify({"error": f"Internal Server Error regarding {table_name} count"}), 500

    finally:
        if conn:
            conn.close()

# Endpoint for site count (No extra condition)
@app.route('/api/get-site-count', methods=['GET'])
def get_site_count():
    """
    Get the count of sites from the Sites table.
    """
    return get_count_from_table('Sites')

#Endpoint for camera count (No extra condition)
@app.route('/api/get-camera-count', methods=['GET'])
def get_camera_count():
    """
    Get the count of cameras from the Cameras table.
    """
    return get_count_from_table('Cameras')

#Endpoint for hazard count (Condition: `falsePositive = 0`)
@app.route('/api/get-hazard-count', methods=['GET'])
def get_hazard_count():
    """
    Get the count of hazards from the Logs table where falsePositive = 0.
    """
    return get_count_from_table('Logs', "falsePositive = %s", (0,))


@app.route('/api/anomalies-by-month', methods=['GET'])
def get_anomalies_by_month():
    """
    Fetches the count of anomalies by month from the Logs table.
    Returns data for the current year's monthly anomaly counts.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Extract year and month from hourTime and count anomalies
            #  hourTime format is "YYYY-MM-DD HH"
            cursor.execute("""
                SELECT
                    SUBSTRING(hourTime, 6, 2) AS month,
                    SUM(number) AS anomaly_count
                FROM Logs
                WHERE SUBSTRING(hourTime, 1, 4) = YEAR(CURDATE())
                GROUP BY SUBSTRING(hourTime, 6, 2)
                ORDER BY month;
            """)
            results = cursor.fetchall()

            # Create a dictionary with all months initialized to 0
            months = {f"{i:02d}": 0 for i in range(1, 13)}

            # Update with actual data
            for month, count in results:
                months[month] = count

            # Convert to list maintaining month order
            monthly_data = [months[f"{i:02d}"] for i in range(1, 13)]

        return jsonify(monthly_data), 200

    except Exception as e:
        print(f"Error fetching anomalies by month: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/anomalies-by-type', methods=['GET'])
def get_anomalies_by_type():
    """
    Fetches the count of anomalies grouped by type from the Logs table.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    hazardType,
                    SUM(number) AS anomaly_count
                FROM Logs
                GROUP BY hazardType
                ORDER BY hazardType;
            """)
            results = cursor.fetchall()

            # Transform results into two lists: types and counts
            types = []
            counts = []

            for hazard_type, count in results:
                types.append(hazard_type)
                counts.append(count)

        return jsonify({"types": types, "counts": counts}), 200

    except Exception as e:
        print(f"Error fetching anomalies by type: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/delete-camera/<int:camera_id>', methods=['DELETE'])
def delete_camera(camera_id):
    """
    Deletes a camera from the database by its ID and stops any associated fire detection process.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # First, get the camera's rtsp_url to stop the fire detection process
            cursor.execute("SELECT rtsp_url FROM Cameras WHERE id = %s", (camera_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Camera not found"}), 404

            rtsp_url = result[0]

            # Delete the camera from the database
            cursor.execute("DELETE FROM Cameras WHERE id = %s", (camera_id,))

            # Check if any rows were affected
            if cursor.rowcount == 0:
                return jsonify({"error": "Camera not found"}), 404

        conn.commit()

        # Stop the fire detection process if it's running
        if rtsp_url in fire_detection_processes:
            process = fire_detection_processes.pop(rtsp_url)
            process.terminate()
            print(f"Stopped fire detection for: {rtsp_url}")

        return jsonify({"message": "Camera deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting camera: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()


@app.route('/api/update-camera/<int:camera_id>', methods=['PUT'])
def update_camera(camera_id):
    """
    Updates camera details in the database.
    If RTSP URL changes, restarts the fire detection process.
    """
    data = request.json
    name = data.get('name')
    rtsp_url = data.get('rtsp_url')
    site_id = data.get('site_id')

    # Check if required fields are provided
    if not any([name, rtsp_url, site_id]):
        return jsonify({"error": "At least one field (name, rtsp_url, or site_id) must be provided"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # First, check if the camera exists and get its current RTSP URL
            cursor.execute("SELECT rtsp_url FROM Cameras WHERE id = %s", (camera_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Camera not found"}), 404

            old_rtsp_url = result[0]

            # Build the update query dynamically based on what fields were provided
            update_query = "UPDATE Cameras SET "
            update_values = []

            if name:
                update_query += "name = %s, "
                update_values.append(name)

            if rtsp_url:
                # Convert tcp:// to rtsp:// if necessary
                if rtsp_url.startswith("tcp://"):
                    rtsp_url = "rtsp://" + rtsp_url[6:]
                update_query += "rtsp_url = %s, "
                update_values.append(rtsp_url)

            if site_id is not None:  # Allow setting to NULL for removing from a site
                update_query += "site_id = %s, "
                update_values.append(site_id)

            # Remove trailing comma and space
            update_query = update_query.rstrip(", ")

            # Add the WHERE clause
            update_query += " WHERE id = %s"
            update_values.append(camera_id)

            # Execute the update
            cursor.execute(update_query, tuple(update_values))

            # Check if any rows were affected
            if cursor.rowcount == 0:
                return jsonify({"error": "No changes were made"}), 400

        conn.commit()

        # If RTSP URL changed, restart the fire detection process
        if rtsp_url and rtsp_url != old_rtsp_url:
            # Stop the old process
            if old_rtsp_url in fire_detection_processes:
                process = fire_detection_processes.pop(old_rtsp_url)
                process.terminate()
                print(f"Stopped fire detection for: {old_rtsp_url}")

            # Start a new process
            process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
            process.start()
            fire_detection_processes[rtsp_url] = process
            print(f"Started fire detection for updated camera: {rtsp_url}")

        return jsonify({"message": "Camera updated successfully"}), 200
    except Exception as e:
        print(f"Error updating camera: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/delete-site/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    """
    Deletes a site from the database.
    Optionally handles associated cameras based on the 'delete_cameras' parameter.
    """
    delete_cameras = request.args.get('delete_cameras', 'false').lower() == 'true'

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            if delete_cameras:
                # Get all cameras associated with this site to stop their fire detection processes
                cursor.execute("SELECT id, rtsp_url FROM Cameras WHERE site_id = %s", (site_id,))
                cameras = cursor.fetchall()

                # Delete all cameras associated with this site
                cursor.execute("DELETE FROM Cameras WHERE site_id = %s", (site_id,))

                # Stop fire detection processes for these cameras
                for _, rtsp_url in cameras:
                    if rtsp_url in fire_detection_processes:
                        process = fire_detection_processes.pop(rtsp_url)
                        process.terminate()
                        print(f"Stopped fire detection for: {rtsp_url}")
            else:
                # Unlink cameras from this site (set site_id to NULL)
                cursor.execute("UPDATE Cameras SET site_id = NULL WHERE site_id = %s", (site_id,))

            # Delete the site
            cursor.execute("DELETE FROM Sites WHERE id = %s", (site_id,))

            # Check if any rows were affected
            if cursor.rowcount == 0:
                return jsonify({"error": "Site not found"}), 404

        conn.commit()
        return jsonify({
            "message": "Site deleted successfully",
            "cameras": "deleted" if delete_cameras else "unlinked"
        }), 200
    except Exception as e:
        print(f"Error deleting site: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

# 4. Update Site Endpoint
@app.route('/api/update-site/<int:site_id>', methods=['PUT'])
def update_site(site_id):
    """
    Updates site details in the database.
    """
    data = request.json
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    location = data.get('location')

    # Check if at least one field is provided
    if not any([name, latitude, longitude, location]):
        return jsonify({"error": "At least one field (name, latitude, longitude, or location) must be provided"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Check if the site exists
            cursor.execute("SELECT id FROM Sites WHERE id = %s", (site_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Site not found"}), 404

            # Build the update query dynamically
            update_query = "UPDATE Sites SET "
            update_values = []

            if name:
                update_query += "name = %s, "
                update_values.append(name)

            if latitude:
                update_query += "latitude = %s, "
                update_values.append(latitude)

            if longitude:
                update_query += "longitude = %s, "
                update_values.append(longitude)

            if location:
                update_query += "location = %s, "
                update_values.append(location)

            # Remove trailing comma and space
            update_query = update_query.rstrip(", ")

            # Add the WHERE clause
            update_query += " WHERE id = %s"
            update_values.append(site_id)

            # Execute the update
            cursor.execute(update_query, tuple(update_values))

            # Check if any rows were affected
            if cursor.rowcount == 0:
                return jsonify({"error": "No changes were made"}), 400

        conn.commit()
        return jsonify({"message": "Site updated successfully"}), 200
    except Exception as e:
        print(f"Error updating site: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """
    Fetches all emails from the CustLogin table.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin")
            emails = [row[0] for row in cursor.fetchall()]
        return jsonify(emails)
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/getName', methods=['GET'])
def get_name():
    """
    Authenticates a user by their email and password.
    """
    email = request.args.get('email')  # Fetch query parameter

    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT Customer.firstname
                FROM Customer
                JOIN CustLogin ON Customer.id = CustLogin.id
                WHERE CustLogin.email = %s;
            """, (email,))

            result = cursor.fetchone()

            if result:
                name = result[0]
                return name
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['GET'])
def login():
    """
    Authenticates a user by their email and password.
    """
    email = request.args.get('emailVar') # Fetch query parameter

    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT hashPWord FROM CustLogin WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                stored_hashed_password = result[0]
                return stored_hashed_password
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/addToCustomer', methods=['POST'])
def add_to_customer():
    """Add a customer to DB"""
    data = request.json.get('items', [])
    if len(data) < 4:
        return jsonify({"error": "Invalid input"}), 400

    first_name, last_name, email, password = data
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        # Ensure the Customer table exists
        conn = get_db_connection()
        with conn.cursor() as cursor:
            create_customer_table = """
            CREATE TABLE IF NOT EXISTS Customer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255)
            );
            """
            cursor.execute(create_customer_table)

            # Ensure the CustLogin table exists
            create_custlogin_table = """
            CREATE TABLE IF NOT EXISTS CustLogin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE,
                hashPWord VARCHAR(255),
                customerID INT,
                FOREIGN KEY (customerID) REFERENCES Customer(id)
            );
            """
            cursor.execute(create_custlogin_table)

            # Insert into Customer table
            cursor.execute("INSERT INTO Customer (firstname, lastname) VALUES (%s, %s)",
                           (first_name, last_name))
            customer_id = cursor.lastrowid

            # Insert into CustLogin table
            cursor.execute(
                "INSERT INTO CustLogin (email, hashPWord, customerID) VALUES (%s, %s, %s)",
                (email, hashed_password, customer_id)
            )

        conn.commit()
        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        print(f"Error adding customer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/sendResetEmail', methods=['POST'])
def send_reset_email():
    """Send a reset password email"""
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

@app.route('/api/sendVerifyEmail', methods=['POST'])
def send_verify_email():
    """Send a verify email"""
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/verified-email?token={token}&email={email}"
        otp_code = ''.join(random.choices(string.digits, k=6))
        send_email(email, "Email Verification", verification_link, otp_code)
        return jsonify({"message": "Verification email sent successfully"})
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

def send_email(to_email, subject, link, code=None):
    """Send an email using the Postmark API"""
    postmark_token = POSTMARK_API  # Client's Postmark server API token
    sender_email = "info@digitalU3.com" # Client's Sender email

    html_content = f"""
    <div>
        <p>Click <a href="{link}">here</a> to proceed.</p>
    """
    if code:
        html_content += f"<p>Your OTP is: <strong>{code}</strong></p>"
    html_content += "</div>"

    payload = {
        "From": sender_email,
        "To": to_email,
        "Subject": subject,
        "HtmlBody": html_content,
        "MessageStream": "verify"
    }

    try:
        url = "https://api.postmarkapp.com/email"
        headers = [
            "Accept: application/json",
            "Content-Type: application/json",
            f"X-Postmark-Server-Token: {postmark_token}"
        ]
        data = json.dumps(payload)
        response_buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, data)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, response_buffer)
        c.setopt(c.TIMEOUT, 30)
        c.perform()
        response_body = response_buffer.getvalue().decode('utf-8')
        c.close()
        print(f"Email sent successfully to {to_email}. With {response_body}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    start_fire_detection_for_all_cameras() # Start fire detection for all cameras on launch
    app.run(host='0.0.0.0', port=3000, debug=True)
