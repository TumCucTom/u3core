from flask_cors import CORS
import bcrypt
import random
import string
import secrets
import pymysql
import pycurl
import requests
from io import BytesIO
import json
import time
import logging
import sys
from flask import Flask, request, jsonify
import multiprocessing
from fire_detection_script import process_rtsp_stream_with_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to Docker console (stdout)
    ]
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration from config.json
def load_db_config(filename="db-config.json"):
    with open(filename, "r") as db_config_file:
        db_config_fi = json.load(db_config_file)
    return db_config_fi

# Retrieve the database configuration
db_config = load_db_config()


max_retries = 10
for attempt in range(max_retries):
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection successful!")
        break
    except pymysql.err.OperationalError as e:
        print(f"Attempt {attempt + 1}/{max_retries}: Unable to connect to the database. Retrying...")
        time.sleep(5)
else:
    raise Exception("Max retries exceeded. Could not connect to the database.")


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
    global fire_detection_processes
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
        with connection.cursor() as cursor:
            # Create the Cameras table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Cameras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                rtsp_url TEXT
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

        # Start fire detection for the new camera
        if rtsp_url not in fire_detection_processes:
            process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
            process.start()
            fire_detection_processes[rtsp_url] = process
            print(f"Started fire detection for new camera: {rtsp_url}")

        return jsonify({"message": "Camera added, TCP URLs updated, and fire detection started!"}), 201
    except Exception as e:
        print(f"Error adding camera: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


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
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/sites', methods=['GET'])
def fetch_sites():
    """
    Fetches all sites and their associated cameras.
    """
    try:
        with connection.cursor() as cursor:
            # Fetch all sites
            cursor.execute("SELECT id, name FROM Sites")
            sites = cursor.fetchall()

            # Fetch cameras for each site
            result = []
            for site in sites:
                site_id, name = site
                cursor.execute("SELECT id, name FROM Cameras WHERE site_id = %s", (site_id,))
                cameras = [{"id": cam_id, "name": cam_name} for cam_id, cam_name in cursor.fetchall()]
                result.append({"id": site_id, "name": name, "cameras": cameras})

        return jsonify({"sites": result}), 200
    except Exception as e:
        print(f"Error fetching sites: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/test', methods=['GET'])
def test_server():
    return jsonify({"message": "Server is running!", "status": "success"}), 200

@app.route('/api/testAddEntry', methods=['POST'])
def test_add_entry():
    test_data = request.json.get('testData', 'Default Test Data')

    try:
        with connection.cursor() as cursor:
            # Create the TestTable if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS TestTable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                testData VARCHAR(255)
            );
            """
            cursor.execute(create_table_query)

            # Insert the test data
            cursor.execute("INSERT INTO TestTable (testData) VALUES (%s)", (test_data,))

        connection.commit()
        return jsonify({"message": "Test entry added successfully!"})
    except Exception as e:
        print(f"Error adding test entry: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/emails', methods=['GET'])
def get_emails():
    """
    Fetches all emails from the CustLogin table.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin")
            emails = [row[0] for row in cursor.fetchall()]
        return jsonify(emails)
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/getName', methods=['GET'])
def get_name():
    """
    Authenticates a user by their email and password.
    """
    email = request.args.get('email')  # Fetch query parameter

    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        with connection.cursor() as cursor:
            # Fetch the name for the given email
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

@app.route('/api/login', methods=['GET'])
def login():
    """
    Authenticates a user by their email and password.
    """
    email = request.args.get('emailVar')  # Fetch query parameter

    if not email:
        return jsonify({"error": "Email required"}), 400

    try:
        with connection.cursor() as cursor:
            # Fetch the hashed password for the given email
            cursor.execute("SELECT hashPWord FROM CustLogin WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                stored_hashed_password = result[0]
                return stored_hashed_password
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/addToCustomer', methods=['POST'])
def add_to_customer():
    data = request.json.get('items', [])
    if len(data) < 4:
        return jsonify({"error": "Invalid input"}), 400

    first_name, last_name, email, password = data
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        with connection.cursor() as cursor:
            # Ensure the Customer table exists
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
            cursor.execute("INSERT INTO Customer (firstname, lastname) VALUES (%s, %s)", (first_name, last_name))
            customer_id = cursor.lastrowid

            # Insert into CustLogin table
            cursor.execute(
                "INSERT INTO CustLogin (email, hashPWord, customerID) VALUES (%s, %s, %s)",
                (email, hashed_password, customer_id)
            )

        connection.commit()
        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        print(f"Error adding customer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



@app.route('/api/sendResetEmail', methods=['POST'])
def send_reset_email():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/ResetPassword?token={token}&email={email}"
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/sendVerifyEmail', methods=['POST'])
def send_verify_email():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustLogin WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/verified-email?token={token}&email={email}"
        otp_code = ''.join(random.choices(string.digits, k=6))
        #return jsonify({"error": send_email(email, "Password Reset Request", verification_link)}), 500
        send_email(email, "Email Verification", verification_link, otp_code)
        return jsonify({"message": "Verification email sent successfully"})
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


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

    # Prepare the payload for the Postmark API
    payload = {
        "From": sender_email,
        "To": to_email,
        "Subject": subject,
        "HtmlBody": html_content,
        "MessageStream": "verify"
    }

    # Send the email using the Postmark API
    try:
        url = "https://api.postmarkapp.com/email"
        headers = [
            "Accept: application/json",
            "Content-Type: application/json",
            f"X-Postmark-Server-Token: {postmark_token}"
        ]

        # Prepare the data
        data = json.dumps(payload)

        # Use BytesIO to capture the response body
        response_buffer = BytesIO()

        # Set up the pycurl request
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, data)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, response_buffer)
        c.setopt(c.TIMEOUT, 30)  # 30 seconds timeout

        # Execute the request
        c.perform()

        # Get the response data
        response_body = response_buffer.getvalue().decode('utf-8')

        # Close the connection
        c.close()

        print(f"Email sent successfully to {to_email}. With {response_body}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {e}")


if __name__ == '__main__':
    start_fire_detection_for_all_cameras()  # Start fire detection for all cameras on launch
    app.run(host='0.0.0.0', port=3000, debug=True)
