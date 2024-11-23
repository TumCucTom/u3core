"""Obtaining and processing frames"""
import sys
import base64
import cv2

#add modules to path
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')

#size of the image you want to send to the network in SIZE x SIZE pixels
SIZE = 416

#change input number from 0 to change the camera in use
RTSP_URL = "rtsp://localhost:8554/mystream"
video = cv2.VideoCapture(RTSP_URL)

def get_image():
    """get the image and process it ready for the roboflow model."""
    # Get the current image from the webcam
    _, img = video.read()
    if img is None:
        print("Failed to capture image")
        return None

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, _ = img.shape
    scale = SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)

    return img_str

# Release resources when finished
video.release()
cv2.destroyAllWindows()
