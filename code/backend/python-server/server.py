from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import bcrypt
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import secrets

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:9000", "supports_credentials": True}})

# Database connection
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "MLAIDB")
}

connection = pymysql.connect(**db_config)


@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM customerLogins")
            emails = [row[0] for row in cursor.fetchall()]
        return jsonify(emails)
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/login', methods=['GET'])
def login():
    email = request.args.get('emailVar')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT encryptedPassword FROM customerLogins WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                return jsonify(result[0])
            return jsonify(None)
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
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/sendResetEmail', methods=['POST'])
def send_reset_email():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email FROM CustomerLogins WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/ResetPassword?token={token}&email={email}"
        send_email(email, "Password Reset Request", verification_link)
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
            cursor.execute("SELECT email FROM CustomerLogins WHERE email = %s", (email,))
            if not cursor.fetchone():
                return jsonify({"message": "Email not found"}), 404

        token = secrets.token_hex(20)
        verification_link = f"http://localhost:9000/#/VerifiedPassword?token={token}&email={email}"
        otp_code = ''.join(random.choices(string.digits, k=6))
        send_email(email, "Email Verification", verification_link, otp_code)
        return jsonify({"message": "Verification email sent successfully"})
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


def send_email(to_email, subject, link, code=None):
    smtp_user = "u3Core@gmail.com"
    smtp_password = "auftest123"
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = to_email
    message['Subject'] = subject

    html_content = f"""
    <div>
        <p>Click <a href="{link}">here</a> to proceed.</p>
    """
    if code:
        html_content += f"<p>Your OTP is: <strong>{code}</strong></p>"
    html_content += "</div>"

    message.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
