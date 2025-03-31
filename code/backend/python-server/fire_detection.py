"""Fire detection processing module"""
import logging
import multiprocessing
from fire_detection_script import process_rtsp_stream_with_url

# Dictionary to track running fire detection processes
fire_detection_processes = {}

def run_fire_detection(rtsp_url):
    """Run the fire detection script for a given RTSP URL."""
    logging.info("Running fire detection on %(url)s", {"url": rtsp_url})
    process_rtsp_stream_with_url(rtsp_url)

def start_fire_detection_for_all_cameras(connection, processes, detection_func):
    """
    Fetch all cameras from the database and start fire detection concurrently.
    Ensures each RTSP stream is monitored independently.

    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT rtsp_url FROM Cameras")
            cameras = cursor.fetchall()
        for (rtsp_url,) in cameras:
            if rtsp_url not in processes:  # Avoid duplicate processes
                process = multiprocessing.Process(target=detection_func, args=(rtsp_url,))
                process.start()
                processes[rtsp_url] = process
                logging.info("Started fire detection for: %(url)s", {"url": rtsp_url})
        logging.info("Started fire detection for all cameras")
    except Exception as error:
        logging.error("Error starting fire detection processes: %(error)s", {"error": error})