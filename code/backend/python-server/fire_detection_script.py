"""
Fire Detection and Alert System

This script captures video from an RTSP stream, detects fire using the Roboflow API,
and sends alerts via AWS SNS (SMS) and Twilio (WhatsApp) when fire is detected.

Configuration values are loaded from `config.json`, which should contain AWS, Twilio,
and Roboflow credentials, as well as recipient contact details.
"""
import os
import time
import datetime
import cv2
import boto3
from twilio.rest import Client
import requests
from dotenv import load_dotenv
# pylint: disable=no-member


# Load environment variables from ../../../.env
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

# Roboflow setup
R_API_KEY = os.getenv("R_API_KEY")
R_MODEL_URL = os.getenv("R_MODEL_URL")
R_CONFIDENCE = 0.5

R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": R_CONFIDENCE
}

# Alert message
ALERT_MESSAGE = "Abnormal detected"

def send_hazard_log(rtsp_url, hazard):
    """
    Sends a POST request to the /api/add-hazard endpoint
    """
    url = "http://127.0.0.1:3000/api/add-hazard"

    # Generate current timestamp in "YYYY-MM-DD HH:MM:SS" format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the request payload
    payload = {
        "timestamp": timestamp,
        "type": hazard,
        "cameraAddress": rtsp_url
    }

    try:
        response = requests.post(url, json=payload, timeout="15")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return {"error": "Failed to send request"}

# Send SMS via AWS SNS
def send_sms_via_sns(phone_number, message):
    """send message via SMS"""
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

# Detect fire using Roboflow
def detect_fire_with_roboflow(frame):
    """Detect fire using Roboflow API."""
    _, img_encoded = cv2.imencode(".jpg", frame)
    response = requests.post(
        R_MODEL_URL,
        params=R_PARAMS,
        files={"file": img_encoded.tobytes()},
        timeout=5.0
    )
    response_data = response.json()
    predictions = response_data.get("predictions", [])

    for prediction in predictions:
        if prediction["class"] == "fire" and prediction["confidence"] >= R_PARAMS["confidence"]:
            return True , "fire"
    return False, "none"

# Process RTSP stream
def process_rtsp_stream_with_url(rtsp_url):
    """Process RTSP stream for fire detection."""
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Unable to open RTSP stream.")
        return

    last_alert_time = 0
    alert_interval = 30

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            break

        fire_detected, alert_type = detect_fire_with_roboflow(frame)

        if fire_detected:
            current_time = time.time()
            if current_time - last_alert_time > alert_interval:
                print("Fire detected! Sending alerts...")
                send_sms_via_sns(REC_NUMBER, ALERT_MESSAGE)
                send_whatsapp_via_twilio(REC_WHATSAPP_NUMBER, ALERT_MESSAGE)

                send_hazard_log(rtsp_url,alert_type)

                last_alert_time = current_time

        cv2.imshow("Webcam Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
