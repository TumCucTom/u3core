"""Camera endpoint handlers"""
import logging
import multiprocessing
from flask import jsonify, request
from database import get_db_connection
from endpoints.endpoint_utils import get_count_from_table

def register_camera_endpoints(app, db_config, fire_detection_processes, run_fire_detection):
    """
    Register all camera related endpoints
    """
    @app.route('/api/add-camera', methods=['POST'])
    def add_camera():
        """
        Adds a new RTSP camera to the database and starts fire detection for it.
        Converts tcp:// to rtsp:// if necessary and updates existing records.
        """
        data = request.json
        name = data.get('name')
        rtsp_url = data.get('rtsp_url')
        site_id = data.get('site_id')

        if not all([name, rtsp_url, site_id]):
            return jsonify({"error": "Name, RTSP URL or site id required"}), 400

        # Convert tcp:// to rtsp://
        if rtsp_url.startswith("tcp://"):
            rtsp_url = "rtsp://" + rtsp_url[6:]

        try:
            # Create the Cameras table if it doesn't exist
            conn = get_db_connection(db_config)
            with conn.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS Cameras (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rtsp_url TEXT,
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
                    "INSERT INTO Cameras (name, rtsp_url,site_id) VALUES (%s, %s,%s)",
                    (name, rtsp_url, site_id)
                )
            conn.commit()

            # Start fire detection for the new camera
            if rtsp_url not in fire_detection_processes:
                process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
                process.start()
                fire_detection_processes[rtsp_url] = process
                logging.info("Started fire detection for new camera: %s", rtsp_url)
            return jsonify(
                {"message": "Camera added, TCP URLs updated, and fire detection started!"}), 201

        except Exception as error:
            logging.error("Error adding camera: %s", error)
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            conn.close()

    @app.route('/api/delete-camera/<int:camera_id>', methods=['DELETE'])
    def delete_camera(camera_id):
        """
        Deletes a camera from the database by its ID and stops any associated fire detection process.
        """
        try:
            conn = get_db_connection(db_config)
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
                logging.info("Stopped fire detection for: %s", rtsp_url)

            return jsonify({"message": "Camera deleted successfully"}), 200
        except Exception as error:
            logging.error("Error deleting camera: %s", error)
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
            conn = get_db_connection(db_config)
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
                    logging.info("Stopped fire detection for: %s", old_rtsp_url)

                # Start a new process
                process = multiprocessing.Process(target=run_fire_detection, args=(rtsp_url,))
                process.start()
                fire_detection_processes[rtsp_url] = process
                logging.info("Started fire detection for updated camera: %s", rtsp_url)

            return jsonify({"message": "Camera updated successfully"}), 200
        except Exception as error:
            logging.error("Error updating camera: %s", error)
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            conn.close()

    @app.route('/api/get-camera-count', methods=['GET'])
    def get_camera_count():
        """
        Get the count of cameras from the Cameras table.
        """
        return get_count_from_table('Cameras', db_config)
