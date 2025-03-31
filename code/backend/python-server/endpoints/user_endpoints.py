"""User endpoint handlers"""
import logging
import random
import string
import secrets
import json
import bcrypt
from flask import jsonify, request
from database import get_db_connection
from email_utils import send_email

def register_user_endpoints(app, db_config, postmark_api):
    """Register all user related endpoints"""

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
