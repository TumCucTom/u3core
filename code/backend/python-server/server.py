from flask import Flask, request, jsonify
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
import cv2
from twilio.rest import Client
import multiprocessing
from fire_detection_script import process_rtsp_stream_with_url
import datetime

# Load configuration from JSON
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# AWS SNS setup
AWS_REGION = config["aws"]["region"]
AWS_ACCESS_KEY = config["aws"]["access_key"]
AWS_SECRET_KEY = config["aws"]["secret_key"]

# Twilio setup
T_ACCOUNT_SID = config["twilio"]["account_sid"]
T_AUTH_TOKEN = config["twilio"]["auth_token"]
TWILO_NUMBER = config["twilio"]["number"]

# Recipient setup
REC_NUMBER = config["recipient"]["phone_number"]
REC_WHATSAPP_NUMBER = config["recipient"]["whatsapp_number"]

# Roboflow setup
R_API_KEY = config["roboflow"]["api_key"]
R_MODEL_URL = config["roboflow"]["model_url"]
R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": config["roboflow"]["confidence"]
}

# Alert message
ALERT_MESSAGE = "Abnormal detected"


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

db_config = {
    "host": "db",
    "user": "general-user",
    "password": "MLAI2024",
    "database": "MLAIDB",
    "port": 3306
}

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
    
# detecting fire with roboflow
def detect_fire_with_roboflow(frame):
    """Detect fire using Roboflow API."""
    _, img_encoded = cv2.imencode(".jpg", frame)
    response = requests.post(
        R_MODEL_URL,
        params=R_PARAMS,
        files={"file": img_encoded.tobytes()},
        timeout=5.0
    )
    response_data = response.json()
    predictions = response_data.get("predictions", [])

    for prediction in predictions:
        if prediction["class"] == "fire" and prediction["confidence"] >= R_PARAMS["confidence"]:
            return True
    return False

# Sending message via whatsapp
def send_whatsapp_via_twilio(to_number, message):
    """Send WhatsApp message via Twilio."""
    client = Client(T_ACCOUNT_SID, T_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILO_NUMBER,
        body=message,
        to=to_number
    )
    print(f"WhatsApp message sent! Message SID: {message.sid}")

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
    
@app.route('/api/stream',methods = ['POST'])
def stream():
    data = request.json
    name = data.get('name')
    rtsp_url = data.get('rtsp_url')

    if not all([name, rtsp_url]):
        return jsonify({"error": "Name and RTSP URL are required"}), 400

    # Convert tcp:// to rtsp://
    if rtsp_url.startswith("tcp://"):
        rtsp_url = "rtsp://" + rtsp_url[6:]

    video = cv2.VideoCapture(rtsp_url)
    if not video.isOpened:
        print("Error : Camera is not opened")
    
    last_alert = 0
    alert_interval = 30

    while True:
        ret,frame = video.read()
        if not ret:
            break
        fire_detected = detect_fire_with_roboflow(frame)
        if fire_detected:
            current_time = time.time()
            if current_time - last_alert > alert_interval:
                print("Sending message")
                send_whatsapp_via_twilio(REC_WHATSAPP_NUMBER,ALERT_MESSAGE)
                last_alert = current_time

        cv2.imshow("webcam stream",frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


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
        with connection.cursor() as cursor:
            # Fetch camera name from the Cameras table
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

        connection.commit()
        return jsonify({"message": "Log added successfully!"}), 201

    except Exception as e:
        print(f"Error adding log: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/get-logs', methods=['GET'])
def get_logs():
    """
    Fetch all hazard log entries from the logs table and return them in a format
    compatible with the front end
    """
    try:
        with connection.cursor() as cursor:
            # Retrieve all log entries sorted by most recent first
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




@app.route('/api/dbinfo', methods=['GET'])
def get_db_info():
    try:
        with connection.cursor() as cursor:
            # Fetch all table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            db_info = {}

            for (table_name,) in tables:
                # Fetch column details for each table
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
                    } for col in columns
                ]

                # Fetch all rows for each table
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                db_info[table_name] = {
                    "columns": column_info,
                    "entries": rows
                }

        return jsonify(db_info)

    except Exception as e:
        print(f"Error fetching database info: {e}")
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
