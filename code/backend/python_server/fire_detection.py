"""Fire detection processing module"""
import logging
import multiprocessing
import pymysql
from python_server.fire_detection_script import run_yolov8_inference

# Dictionary to track running fire detection processes
fire_detection_processes = {}

def run_fire_detection(rtsp_url,
                       number,
                       conf=0.6,
                       iou=0.5,
                       alert_class="fire",
                       alert_interval=10,
                       model_path = "models/default/best.pt"):
    """Run the fire detection script for a given RTSP URL."""
    logging.info("Running fire detection on {rtsp_url}")
    run_yolov8_inference(rtsp_url,number,conf,iou,alert_class,alert_interval,model_path)

def start_fire_detection_for_all_cameras(connection, processes, detection_func):
    """
    Fetch all cameras from the database and start fire detection concurrently.
    Ensures each RTSP stream is monitored independently.

    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT rtsp_url,number,model FROM Cameras")
            cameras = cursor.fetchall()
        for (rtsp_url,number,model) in cameras:
            if rtsp_url not in processes:  # Avoid duplicate processes
                process = multiprocessing.Process(target=detection_func,
                                                  args=(rtsp_url,number,0.6,0.5,"fire",10,f'models/{model}/best.pt',))
                process.start()
                processes[rtsp_url] = process
                logging.info("Started fire detection for: %(url)s", {"url": rtsp_url})
        logging.info("Started fire detection for all cameras")
    except (pymysql.Error, RuntimeError, ValueError) as error:
        logging.error("Error starting fire detection processes: %(error)s", {"error": error})
        