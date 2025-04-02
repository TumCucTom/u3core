"""Hazard/logs endpoint handlers"""
import logging
from datetime import datetime
from flask import jsonify, request
from database import get_db_connection
from endpoints.endpoint_utils import get_count_from_table

def register_hazard_endpoints(app, db_config):
    """
    Register all hazard/logs related endpoints
    """
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
            conn = get_db_connection(db_config)
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

        except Exception as error:
            logging.error("Error adding log: %s", error)
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
            conn = get_db_connection(db_config)
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

        except Exception as error:
            logging.error("Error retrieving logs: %s", error)
            return jsonify({"error": "Internal Server Error"}), 500

        finally:
            conn.close()

    @app.route('/api/get-hazard-count', methods=['GET'])
    def get_hazard_count():
        """
        Get the count of hazards from the Logs table where falsePositive = 0.
        """
        return get_count_from_table('Logs', db_config, "falsePositive = %s", (0,))
