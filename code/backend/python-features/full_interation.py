"""all features integrated into one script"""
import time
import cv2
import boto3
from twilio.rest import Client
import requests

# AWS SNS set up
AWS_REGION = "aws_region"
AWS_ACESS_KEY = "aws_access_key"
AWS_SECRET_KEY = "aws_secret_key"

# Twilio set up
T_ACCOUNT_SID = "twilio_account_sid"
T_AUTH_TOKEN = "twilio_auth_token"
TWILO_NUMBER = "twilio_whatsapp_number"

# Recipient set up
REC_NUMBER = "number"
REC_WHATSAPP_NUMBER = "whatsapp:number"


# Roboflow set up
R_API_KEY ="FRUmKXAzM8M7TupHxPph"
R_MODEL_URL = "https://app.roboflow.com/tumcuc/people-in-a-room-counter-2/3"
R_PARAMS = {
    "api_key": R_API_KEY,
    "confidence": 0.5
}

# RTSP streaming URL
RTSP_URL = "rtsp://x.x.x.x:8554/mystream"

# Alert message
ALERT_MESSAGE = "Abnormal detected"

# send message through Aws sns(must be implemented)
def send_sms_via_sns(phone_number, message):
    """Send SMS via AWS SNS."""
    sns_client = boto3.client(
        "sns",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACESS_KEY,
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


#Get Streaming from RTSP
def process_rtsp_stream():
    """Process RTSP stream for fire detection."""
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print("Error: Unable to open RTSP stream.")
        return

    last_alert_time = 0  # To prevent frequent alerts
    alert_interval = 30  # Send alerts every 30 seconds if fire persists

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
    process_rtsp_stream()
