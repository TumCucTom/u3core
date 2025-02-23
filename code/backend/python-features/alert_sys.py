"""Alert users when a user when a hazard is detected"""
import time
import os
import cv2
import boto3
from twilio.rest import Client
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS SNS set up
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# Twilio set up
T_ACCOUNT_SID = os.getenv("T_ACCOUNT_SID")
T_AUTH_TOKEN = os.getenv("T_AUTH_TOKEN")
TWILO_NUMBER = os.getenv("TWILO_NUMBER")

# Recipient set up
REC_NUMBER = os.getenv("REC_NUMBER")
REC_WHATSAPP_NUMBER = os.getenv("REC_WHATSAPP_NUMBER")

# Roboflow set up
R_API_KEY = os.getenv("R_API_KEY")
R_MODEL_URL = os.getenv("R_MODEL_URL")
R_CONFIDENCE = float(os.getenv("R_CONFIDENCE"))  # Default to 0.5 if not set
R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": R_CONFIDENCE
}

# RTSP Streaming URL (if needed)
# RTSP_URL = os.getenv("RTSP_URL")

# Alert message
ALERT_MESSAGE = os.getenv("ALERT_MESSAGE", "Abnormal detected")

# Send message through AWS SNS
def send_sms_via_sns(phone_number, message):
    """Send SMS via AWS SNS."""
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

# Send message through Twilio
def send_whatsapp_via_twilio(to_number, message):
    """Send WhatsApp message via Twilio."""
    client = Client(T_ACCOUNT_SID, T_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILO_NUMBER,
        body=message,
        to=to_number
    )
    print(f"WhatsApp message sent! Message SID: {message.sid}")

# Detect fire by using Roboflow
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
            return True
    return False

# Process webcam stream
def process_webcam_stream():
    """Process webcam stream for fire detection."""
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return
    last_alert_time = 0
    alert_interval = 30

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            break

        fire_detected = detect_fire_with_roboflow(frame)

        if fire_detected:
            current_time = time.time()
            if current_time - last_alert_time > alert_interval:
                print("Fire detected! Sending alerts...")
                send_sms_via_sns(REC_NUMBER, ALERT_MESSAGE)
                send_whatsapp_via_twilio(REC_WHATSAPP_NUMBER, ALERT_MESSAGE)
                last_alert_time = current_time

        cv2.imshow("Webcam Stream", frame)  # Show webcam stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_webcam_stream()
    