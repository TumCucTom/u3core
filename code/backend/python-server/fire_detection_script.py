"""
Fire Detection and Alert System (YOLOv8)

This script captures video from an RTSP stream, detects fire using a trained YOLOv8 model,
and sends alerts via AWS SNS (SMS) and Twilio (WhatsApp) when fire is detected.

Configuration values are loaded from environment variables.
"""
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=redefined-outer-name
import os
import datetime
import time
import requests
from dotenv import load_dotenv
import cv2
from ultralytics import YOLO
from twilio.rest import Client

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(dotenv_path)

# Twilio setup
T_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
T_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Alert message
ALERT_MESSAGE = "Fire detected! Immediate action required!"

def send_whatsapp_via_twilio(number, stream_address, datetime):
    """Send WhatsApp message via Twilio."""
    account_sid = T_ACCOUNT_SID
    auth_token = T_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_ ='whatsapp:+14155238886',
        body =f'Fire Detected -  site: test123, rtsp: {stream_address}, time: {datetime}',
        to=f'whatsapp:{number}'
    )

    print(message.sid)

def send_hazard_log(rtsp_url, hazard):
    """
    Sends a POST request to the /api/add-hazard endpoint
    """
    url = "http://16.171.224.57:0080/api/add-hazard"

    # Generate current timestamp in "YYYY-MM-DD HH:MM:SS" format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the request payload
    payload = {
        "timestamp": timestamp,
        "type": hazard,
        "cameraAddress": rtsp_url
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return {"error": "Failed to send request"}


# Detect fire using YOLOv8
def detect_fire_with_yolo(frame, model):
    """Detect fire using the trained YOLOv8 model."""
    results = model(frame)  # Run inference on the frame
    detections = results[0].boxes  # Get detected bounding boxes

    for box in detections:
        class_id = int(box.cls[0].item())  # Get class index
        confidence = box.conf[0].item()  # Get confidence score

        if class_id == 0 and confidence >= 0.6:  # Assuming 'fire' is class 0
            return True, "fire"

    return False, "none"


def run_yolov8_inference(rtsp_url,
                         number,
                         conf=0.6,
                         iou=0.5,
                         alert_class="fire",
                         alert_interval=10,
                         model_path = "models/default/best.pt"
                         ):
    """
    Run YOLOv8 inference on webcam or RTSP input, detect 'fire', and trigger alerts.

    Args:
        rtsp_url: the address of stream
        number: phone number to whatsapp
        conf: Confidence threshold.
        iou: IOU threshold.
        alert_class: Class name to trigger alert.
        alert_interval: Seconds between repeated alerts.
        model_path: path to the stored model
    """
    model = YOLO(model_path)

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Unable to open RTSP stream.")
        return

    last_alert_time = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run inference
        results = model(frame, conf=conf, iou=iou, verbose=False)

        # Fire alert logic
        fire_detected = False
        for box in results[0].boxes.data:
            class_id = int(box[5].item())
            class_name = model.names[class_id]
            if class_name.lower() == alert_class.lower():
                fire_detected = True
                break

        if fire_detected:
            current_time = time.time()
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if current_time - last_alert_time > alert_interval:
                print("Fire detected! Sending alerts...")
                last_alert_time = current_time
                send_whatsapp_via_twilio(number,rtsp_url,date_time)
                send_hazard_log(rtsp_url, "fire")

    cap.release()
    cv2.destroyAllWindows()
