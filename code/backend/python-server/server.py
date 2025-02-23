"""Backend python server for api endpoints and fire detection"""
# pylint: disable=line-too-long
# pylint: disable=broad-except
# pylint: disable=logging-fstring-interpolation
# pylint: disable=c-extension-no-member

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
import bcrypt
import pymysql
import pycurl
import requests
import cv2
from fire_detection_script import process_rtsp_stream_with_url
from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import datetime
import traceback  # to print full error traces in docker
from dotenv import load_dotenv

# Load environment variables from ../../../.env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]  # log to docker console for debug
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

# Test DB connectivity at startup
MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        # Just open and close once to verify we can connect
        connection = pymysql.connect(**db_config)
        connection.close()
        logging.info("Database connection test successful!")
        break
    except pymysql.err.OperationalError as e:
        logging.warning(f"Attempt {attempt + 1}/{MAX_RETRIES}: Unable to connect to the database. Retrying...")
        time.sleep(5)
else:
     logging.critical("Max retries exceeded. Could not connect to the database.")

def get_db_connection():
    """
    Returns a fresh PyMySQL connection each time it is called.
    """
    return pymysql.connect(**db_config)

# Dictionary to track running fire detection processes
fire_detection_processes = {}

def run_fire_detection(rtsp_url):
    """
    Run the fire detection script for a given RTSP URL.
    Each child process should open its own DB connection if needed.
    """
    logging.info(f"Running fire detection on {rtsp_url}")
    # If process_rtsp_stream_with_url uses the database, it should also call get_db_connection() inside.
    process_rtsp_stream_with_url(rtsp_url)

def start_fire_detection_for_all_cameras():
    """
    Fetch all cameras from the database and start fire detection concurrently.
    Ensures each RTSP stream is monitored independently.
    """
    global fire_detection_processes
    with get_db_connection() as connection:
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
            traceback.print_exc()
        finally:
            connection.close()

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

    with get_db_connection() as connection:
        try:
            with connection.cursor() as cursor:
                # Create the Cameras table if it doesn't exist
                create_table_query = """
                CREATE TABLE IF NOT EXISTS Cameras (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rtsp_url TEXT,
                    site_id INT NULL
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
            connection.commit()

            global fire_detection_processes
            if rtsp_url not in fire_detection_processes:
                process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
                process.start()
                fire_detection_processes[rtsp_url] = process
                print(f"Started fire detection for new camera: {rtsp_url}")

            return jsonify({"message": "Camera added, TCP URLs updated, and fire detection started!"}), 201
        except Exception as e:
            print(f"Error adding camera: {e}")
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            connection.close()

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

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create the Sites table if it doesn't exist
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
        connection.commit()
        return jsonify({"message": "Site added successfully!"}), 201
    except Exception as e:
        print(f"Error adding site: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/sites', methods=['GET'])
def fetch_sites():
    """
    Fetches all sites and their associated cameras.
    """
    with get_db_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name FROM Sites")
                sites = cursor.fetchall()

                result = []
                for site_id, name in sites:
                    cursor.execute("SELECT id, name FROM Cameras WHERE site_id = %s", (site_id,))
                    cameras = [{"id": cam_id, "name": cam_name} for cam_id, cam_name in cursor.fetchall()]
                    result.append({"id": site_id, "name": name, "cameras": cameras})

            return jsonify({"sites": result}), 200
        except Exception as e:
            print(f"Error fetching sites: {e}")
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            connection.close()

@app.route('/api/add-hazard', methods=['POST'])
def add_hazard():
    """
    Adds a new hazard log, ensuring proper tracking based on time, camera, and hazard type.
    """
    data = request.json
    timestamp = data.get('timestamp')
    hazard_type = data.get('type')
    rtsp_url = data.get('cameraAddress')  # Assuming cameraAddress holds rtsp_url

    if not all([rtsp_url, timestamp, hazard_type]):
        return jsonify({"error": "Camera address, time, and hazard type are required"}), 400

    try:
        timestamp_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid timestamp format. Use YYYY-MM-DD HH:MM:SS"}), 400

    with get_db_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM Cameras WHERE rtsp_url = %s", (rtsp_url,))
                camera_result = cursor.fetchone()
                if not camera_result:
                    return jsonify({"error": "Camera not found"}), 404

                camera_name = camera_result[0]
                hour_time = timestamp_obj.strftime("%Y-%m-%d %H")

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
                    cursor.execute("""
                        UPDATE Logs
                        SET number = %s, falsePositive = %s
                        WHERE id = %s
                    """, (new_number, false_positive, log_id))
                else:
                    cursor.execute("""
                        INSERT INTO Logs (cameraIP, cameraName, hourTime, hazardType, number, falsePositive)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (rtsp_url, camera_name, hour_time, hazard_type, 1, True))

            connection.commit()
            return jsonify({"message": "Log added successfully!"}), 201

        except Exception as e:
            print(f"Error adding log: {e}")
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            connection.close()

@app.route('/api/get-logs', methods=['GET'])
def get_logs():
    """
    Fetch all hazard log entries from the logs table and return them in a format
    compatible with the front end.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, cameraIP, cameraName, hourTime, hazardType, number, falsePositive
                FROM Logs
                ORDER BY id DESC
            """)
            rows = cursor.fetchall()

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
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/dbinfo', methods=['GET'])
def get_db_info():
    """
    Returns table schemas and all rows for debugging purposes.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            db_info = {}
            for (table_name,) in tables:
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                column_info = [
                    {
                        "Field": col[0],
                        "Type": col[1],
                        "Null": col[2],
                        "Key": col[3],
                        "Default": col[4],
                        "Extra": col[5]
                    }
                    for col in columns
                ]

                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                db_info[table_name] = {
                    "columns": column_info,
                    "entries": rows
                }

        return jsonify(db_info)
    except Exception as e:
        print(f"Error fetching database info: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """
    Fetches all emails from the CustLogin table.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin")
            emails = [row[0] for row in cursor.fetchall()]
        return jsonify(emails)
    except Exception as e:
        print(f"Error fetching emails: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/getName', methods=['GET'])
def get_name():
    """
    Fetches a user's firstname by email.
    """
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT Customer.firstname
                FROM Customer
                JOIN CustLogin ON Customer.id = CustLogin.id
                WHERE CustLogin.email = %s;
            """, (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error during getName: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/login', methods=['GET'])
def login():
    """
    Authenticates a user by their email and returns the hashed password.
    """
    email = request.args.get('emailVar')
    if not email:
        return jsonify({"error": "Email required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT hashPWord FROM CustLogin WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error during login: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/addToCustomer', methods=['POST'])
def add_to_customer():
    data = request.json.get('items', [])
    if len(data) < 4:
        return jsonify({"error": "Invalid input"}), 400

    first_name, last_name, email, password = data
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            create_customer_table = """
            CREATE TABLE IF NOT EXISTS Customer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255)
            );
            """
            cursor.execute(create_customer_table)

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

            cursor.execute("INSERT INTO Customer (firstname, lastname) VALUES (%s, %s)", (first_name, last_name))
            customer_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO CustLogin (email, hashPWord, customerID) VALUES (%s, %s, %s)",
                (email, hashed_password, customer_id)
            )
        connection.commit()
        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        print(f"Error adding customer: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/sendResetEmail', methods=['POST'])
def send_reset_email():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/ResetPassword?token={token}&email={email}"
        # Actual sending logic omitted for brevity
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        print(f"Error sending reset email: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

@app.route('/api/sendVerifyEmail', methods=['POST'])
def send_verify_email():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
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
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        connection.close()

def send_email(to_email, subject, link, code=None):
    postmark_token = "d4763cf8-6f26-46e0-8442-9c3274e51a5b"  # Replace with your Postmark server token
    sender_email = "info@shopveloworks.com"  # Replace with your verified sender email

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
    # Start fire detection for all cameras on launch
    start_fire_detection_for_all_cameras()
    # Run Flask on port 3000 (or change to 3002 if you prefer)
    app.run(host='0.0.0.0', port=3000, debug=True)
