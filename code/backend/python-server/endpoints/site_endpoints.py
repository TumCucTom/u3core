"""Site endpoint handlers"""
import logging
from flask import jsonify, request
from database import get_db_connection

def register_site_endpoints(app, db_config, fire_detection_processes):
    """Register all site related endpoints"""

    @app.route('/api/add-site', methods=['POST'])
    def add_site():
        # Copy the add_site function from server.py
        pass

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


    @app.route('/api/get-site-count', methods=['GET'])
    def get_site_count():
        """
        Get the count of sites from the Sites table.
        """
        return get_count_from_table('Sites')