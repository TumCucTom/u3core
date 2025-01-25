import time
import cv2
import boto3
from twilio.rest import Client
import requests
import json

# Load configuration from JSON
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# AWS SNS setup
AWS_REGION = config["aws"]["region"]
AWS_ACCESS_KEY = config["aws"]["access_key"]
AWS_SECRET_KEY = config["aws"]["secret_key"]

# Twilio setup
T_ACCOUNT_SID = config["twilio"]["account_sid"]
T_AUTH_TOKEN = config["twilio"]["auth_token"]
TWILO_NUMBER = config["twilio"]["number"]

# Recipient setup
REC_NUMBER = config["recipient"]["phone_number"]
REC_WHATSAPP_NUMBER = config["recipient"]["whatsapp_number"]

# Roboflow setup
R_API_KEY = config["roboflow"]["api_key"]
R_MODEL_URL = config["roboflow"]["model_url"]
R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": config["roboflow"]["confidence"]
}

# Alert message
ALERT_MESSAGE = "Abnormal detected"

# Send SMS via AWS SNS
def send_sms_via_sns(phone_number, message):
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
    client = Client(T_ACCOUNT_SID, T_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILO_NUMBER,
        body=message,
        to=to_number
    )
    print(f"WhatsApp message sent! Message SID: {message.sid}")

# Detect fire using Roboflow
def detect_fire_with_roboflow(frame):
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

# Process RTSP stream
def process_rtsp_stream_with_url(rtsp_url):
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

        fire_detected = detect_fire_with_roboflow(frame)

        if fire_detected:
            current_time = time.time()
            if current_time - last_alert_time > alert_interval:
                print("Fire detected! Sending alerts...")
                send_sms_via_sns(REC_NUMBER, ALERT_MESSAGE)
                send_whatsapp_via_twilio(REC_WHATSAPP_NUMBER, ALERT_MESSAGE)
                last_alert_time = current_time

        cv2.imshow("Webcam Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Send SMS via AWS SNS
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
