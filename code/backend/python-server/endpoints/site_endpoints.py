"""Site endpoint handlers"""
import logging
from flask import jsonify, request
from database import get_db_connection
from endpoints.endpoint_utils import get_count_from_table

def register_site_endpoints(app, db_config, fire_detection_processes):
    """
    Register all site related endpoints
    """
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
            conn = get_db_connection(db_config)
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
        except Exception as error:
            logging.error("Error adding site: %s", error)
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
            conn = get_db_connection(db_config)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM Sites")
                sites = cursor.fetchall()

                # Fetch cameras for each site
                result = []
                for site in sites:
                    site_id, name = site
                    cursor.execute(
                        "SELECT id, name FROM Cameras WHERE site_id = %s", (site_id,))
                    cameras = [{"id": cam_id, "name": cam_name}
                              for cam_id, cam_name in cursor.fetchall()]
                    result.append({"id": site_id, "name": name, "cameras": cameras})

            return jsonify({"sites": result}), 200
        except Exception as error:
            logging.error("Error fetching sites: %s", error)
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
            conn = get_db_connection(db_config)
            with conn.cursor() as cursor:
                if delete_cameras:
                    # Get all cameras associated with this site to stop their fire detection processes
                    cursor.execute(
                        "SELECT id, rtsp_url FROM Cameras WHERE site_id = %s",
                        (site_id,)
                    )
                    cameras = cursor.fetchall()

                    # Delete all cameras associated with this site
                    cursor.execute("DELETE FROM Cameras WHERE site_id = %s", (site_id,))

                    # Stop fire detection processes for these cameras
                    for _, rtsp_url in cameras:
                        if rtsp_url in fire_detection_processes:
                            process = fire_detection_processes.pop(rtsp_url)
                            process.terminate()
                            logging.info("Stopped fire detection for: %s", rtsp_url)
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
        except Exception as error:
            logging.error("Error deleting site: %s", error)
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            conn.close()

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
            return jsonify({
                "error": "At least one field (name, latitude, longitude, or location) must be provided"
            }), 400

        try:
            conn = get_db_connection(db_config)
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
        except Exception as error:
            logging.error("Error updating site: %s", error)
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            conn.close()

    @app.route('/api/get-site-count', methods=['GET'])
    def get_site_count():
        """
        Get the count of sites from the Sites table.
        """
        return get_count_from_table('Sites', db_config)
