from flask import Flask, request, jsonify,Response
from flask_cors import CORS
import bcrypt
import random
import string
import secrets
import time
import pymysql
import logging
import pycurl
import requests
from io import BytesIO
import json
from twilio.rest import Client
import cv2

# AWS SNS set up
AWS_REGION = "aws_region"
AWS_ACESS_KEY = "aws_access_key"
AWS_SECRET_KEY = "aws_secret_key"

# Twilio set up
T_ACCOUNT_SID = "twilio_account_sid"
T_AUTH_TOKEN = "twilio_auth_token"
TWILO_NUMBER = "twilio_whatsapp_number"

# Recipient set up
REC_NUMBER = "number"
REC_WHATSAPP_NUMBER = "whatsapp:number"


# Roboflow set up
R_API_KEY ="OQUMCshci7SNfgmSiNDY"
R_MODEL_URL = "https://detect.roboflow.com/u3core-apy5i/2"
R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": 0.5
}

# RTSP streaming URL
RTSP_URL = "rtsp://x.x.x.x:8554/mystream"

# Alert message
ALERT_MESSAGE = "Abnormal detected"



# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Console output
                        logging.FileHandler('/app/logs/myapp.log')  # Log to a file
                    ])

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
    
@app.route('/api/stream',methods = ['GET'])
def stream():
    video = cv2.VideoCapture(RTSP_URL)
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
if __name__ == "__main__":
    stream()




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
    app.run(host='0.0.0.0', port=3000, debug=True)
