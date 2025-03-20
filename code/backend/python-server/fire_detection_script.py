"""
Fire Detection and Alert System (YOLOv8)

This script captures video from an RTSP stream, detects fire using a trained YOLOv8 model,
and sends alerts via AWS SNS (SMS) and Twilio (WhatsApp) when fire is detected.

Configuration values are loaded from environment variables.
"""
import os
import time
import datetime
import cv2
import boto3
from twilio.rest import Client
import requests
from dotenv import load_dotenv
from ultralytics import YOLO

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(dotenv_path)

# AWS SNS setup
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# Twilio setup
T_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
T_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Recipient setup
REC_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")
REC_WHATSAPP_NUMBER = os.getenv("RECIPIENT_WHATSAPP_NUMBER")

# Alert message
ALERT_MESSAGE = "Fire detected! Immediate action required!"

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

# Send SMS via AWS SNS
def send_sms_via_sns(phone_number, message):
    """Send message via SMS."""
    sns_client = boto3.client(
        "sns",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    response = sns_client.publish(
        PhoneNumber=phone_number,
        Message=message
    )
    print(f"SMS sent! Message ID: {response['MessageId']}")

# Send WhatsApp message via Twilio
def send_whatsapp_via_twilio(to_number, message):
    """Send WhatsApp message via Twilio."""
    client = Client(T_ACCOUNT_SID, T_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILO_NUMBER,
        body=message,
        to=to_number
    )
    print(f"WhatsApp message sent! Message SID: {message.sid}")

# Detect fire using YOLOv8
def detect_fire_with_yolo(frame, model):
    """Detect fire using the trained YOLOv8 model."""
    results = model(frame)  # Run inference on the frame
    detections = results[0].boxes  # Get detected bounding boxes

    for box in detections:
        class_id = int(box.cls[0].item())  # Get class index
        confidence = box.conf[0].item()  # Get confidence score

        if class_id == 0 and confidence >= 0.5:  # Assuming 'fire' is class 0
            return True, "fire"

    return False, "none"

# Process RTSP stream
def process_rtsp_stream_with_url(rtsp_url,model_path = "models/default/default.pt" ):
    """Process RTSP stream for fire detection."""
    # Load trained YOLOv8 model
    model = YOLO(model_path)

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Unable to open RTSP stream.")
        return

    last_alert_time = 0
    alert_interval = 30  # Minimum time between alerts (seconds)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from RTSP stream.")
            break

        fire_detected, alert_type = detect_fire_with_yolo(frame, model)

        if fire_detected:
            current_time = time.time()
            if current_time - last_alert_time > alert_interval:
                print("Fire detected! Sending alerts...")
                send_sms_via_sns(REC_NUMBER, ALERT_MESSAGE)
                send_whatsapp_via_twilio(REC_WHATSAPP_NUMBER, ALERT_MESSAGE)
                send_hazard_log(rtsp_url, alert_type)

                last_alert_time = current_time

        # Display the stream with fire detection
        cv2.imshow("Fire Detection Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
