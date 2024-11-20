import cv2
import boto3
from twilio.rest import Client
import time
import requests

# AWS SNS set up
aws_region = "aws_region"
aws_access_key = "aws_access_key"
aws_secret_key = "aws_secret_key"

# Twilio set up
twilio_account_sid = "twilio_account_sid"
twilio_auth_token = "twilio_auth_token"
twilio_whatsapp_number = "twilio_whatsapp_number"

# Recipient set up
recipient_phone_number = "number"
recipient_whatsapp_number = "whatsapp:number"


# Roboflow set up
roboflow_api_key = "roboflow api key"
roboflow_model_url = "model URL"
roboflow_params = {
    "api_key": roboflow_api_key,
    "confidence": 0.5
}

# RTSP streaming URL
# rtsp_url = "rtsp://your_rtsp_stream_url"

# Alert message
alert_message = "Abnormal detected"

# send message through Aws sns(must be implemented)
def send_sms_via_sns(phone_number, message):
    """Send SMS via AWS SNS."""
    sns_client = boto3.client(
        "sns",
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    response = sns_client.publish(
        PhoneNumber=phone_number,
        Message=message
    )
    print(f"SMS sent! Message ID: {response['MessageId']}")

# Send message through Twilio
def send_whatsapp_via_twilio(to_number, message):
    """Send WhatsApp message via Twilio."""
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        body=message,
        to=to_number
    )
    print(f"WhatsApp message sent! Message SID: {message.sid}")


# Detect fire by using Roboflow
def detect_fire_with_roboflow(frame):
    """Detect fire using Roboflow API."""
    _, img_encoded = cv2.imencode(".jpg", frame)
    response = requests.post(
        roboflow_model_url,
        params=roboflow_params,
        files={"file": img_encoded.tobytes()}
    )
    response_data = response.json()
    predictions = response_data.get("predictions", [])

    for prediction in predictions:
        if prediction["class"] == "fire" and prediction["confidence"] >= roboflow_params["confidence"]:
            return True
    return False



# Temporarily using webcam instead of RTSP
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
                send_sms_via_sns(recipient_phone_number, alert_message)
                send_whatsapp_via_twilio(recipient_whatsapp_number, alert_message)
                last_alert_time = current_time

        cv2.imshow("Webcam Stream", frame)  # Show webcam stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_webcam_stream()


# Get Streaming from RTSP
# def process_rtsp_stream():
#     """Process RTSP stream for fire detection."""
#     cap = cv2.VideoCapture(rtsp_url)
#     if not cap.isOpened():
#         print("Error: Unable to open RTSP stream.")
#         return

#     # last_alert_time = 0  # To prevent frequent alerts
#     # alert_interval = 30  # Send alerts every 30 seconds if fire persists

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Unable to read frame from RTSP stream.")
#             break

#         # Use Roboflow to detect fire
#         fire_detected = detect_fire_with_roboflow(frame)

#         if fire_detected:
#             # current_time = time.time()
#             # if current_time - last_alert_time > alert_interval:
#                 print("Fire detected! Sending alerts...")
#                 send_sms_via_sns(recipient_phone_number, alert_message)
#                 send_whatsapp_via_twilio(recipient_whatsapp_number, alert_message)
#                 # last_alert_time = current_time

#         cv2.imshow("RTSP Stream", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     process_rtsp_stream()
