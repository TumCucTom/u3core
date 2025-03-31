"""Analytics endpoint handlers"""
from flask import jsonify
from database import get_db_connection

def register_analytics_endpoints(app, db_config):
    """
    Register all analytics related endpoints
    """
    @app.route('/api/anomalies-by-month', methods=['GET'])
    def get_anomalies_by_month():
        """
        Fetches the count of anomalies by month from the Logs table.
        Returns data for the current year's monthly anomaly counts.
        """
        try:
            conn = get_db_connection(db_config)
            with conn.cursor() as cursor:
                # Extract year and month from hourTime and count anomalies
                #  hourTime format is "YYYY-MM-DD HH"
                cursor.execute("""
                    SELECT
                        SUBSTRING(hourTime, 6, 2) AS month,
                        SUM(number) AS anomaly_count
                    FROM Logs
                    WHERE SUBSTRING(hourTime, 1, 4) = YEAR(CURDATE())
                    GROUP BY SUBSTRING(hourTime, 6, 2)
                    ORDER BY month;
                """)
                results = cursor.fetchall()

                # Create a dictionary with all months initialized to 0
                months = {f"{i:02d}": 0 for i in range(1, 13)}

                # Update with actual data
                for month, count in results:
                    months[month] = count

                # Convert to list maintaining month order
                monthly_data = [months[f"{i:02d}"] for i in range(1, 13)]

            return jsonify(monthly_data), 200

        except Exception as error:
            return jsonify({"error": f"Internal Server Error: {error}"}), 500
        finally:
            conn.close()

    @app.route('/api/anomalies-by-type', methods=['GET'])
    def get_anomalies_by_type():
        """
        Fetches the count of anomalies grouped by type from the Logs table.
        """
        try:
            conn = get_db_connection(db_config)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        hazardType,
                        SUM(number) AS anomaly_count
                    FROM Logs
                    GROUP BY hazardType
                    ORDER BY hazardType;
                """)
                results = cursor.fetchall()

                # Transform results into two lists: types and counts
                types = []
                counts = []

                for hazard_type, count in results:
                    types.append(hazard_type)
                    counts.append(count)

            return jsonify({"types": types, "counts": counts}), 200

        except Exception as error:
            return jsonify({"error": f"Internal Server Error: {error}"}), 500
        finally:
            conn.close()