"""Database connection and initialization module"""
import logging
import pymysql

def get_db_connection(db_config):
    """Return a fresh connection to the database."""
    return pymysql.connect(**db_config)

def initialise_database(db_config):
    """Create all required tables if they don't exist."""
    try:
        conn = get_db_connection(db_config)
        with conn.cursor() as cursor:
            # Create Sites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Sites (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    latitude VARCHAR(50),
                    longitude VARCHAR(50)
                );
            """)

            # Create Cameras table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cameras (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    rtsp_url TEXT,
                    site_id INT,
                    FOREIGN KEY (site_id) REFERENCES Sites(id)
                );
            """)

            # Create Logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cameraIP VARCHAR(255),
                    cameraName VARCHAR(255),
                    hourTime VARCHAR(50),
                    hazardType VARCHAR(50),
                    number INT DEFAULT 1,
                    falsePositive BOOLEAN DEFAULT FALSE
                );
            """)

            # Create Customer and CustLogin tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Customer (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    firstname VARCHAR(255),
                    lastname VARCHAR(255)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS CustLogin (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE,
                    hashPWord VARCHAR(255),
                    customerID INT,
                    FOREIGN KEY (customerID) REFERENCES Customer(id)
                );
            """)

        conn.commit()
        logging.info("Database tables initialized successfully")
    except (pymysql.Error, pymysql.Warning) as error:
        logging.error("Error initializing database tables: %(error)s", {"error": error})
    finally:
        conn.close()
