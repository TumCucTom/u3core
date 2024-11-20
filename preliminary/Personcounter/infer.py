"""Put bounding boxes around people in a room"""
import sys
import base64
import cv2
import numpy as np
import requests

#for the NN we trained on the dataset that can be found under /dataset
ROBOFLOW_API_KEY = "FRUmKXAzM8M7TupHxPph"
ROBOFLOW_MODEL = "people-in-a-room-counter-2"
ROBOFLOW_SIZE = 416

#below needed on my system but unlikely for others
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')

UPLOAD_URL = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?access_token=",
    ROBOFLOW_API_KEY,
    "&format=image",
    "&stroke=5"
])

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)


def infer():
    """Infer via the Roboflow Infer API and return the result"""
    # Get the current image from the webcam
    _, img = video.read()

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, _ = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)

    # Get prediction from Roboflow Infer API
    resp = requests.post(UPLOAD_URL, data=img_str, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, stream=True,timeout=5.0).raw

    # Parse result image
    new_image = np.asarray(bytearray(resp.read()), dtype="uint8")
    new_image = cv2.imdecode(new_image, cv2.IMREAD_COLOR)

    return new_image

# Main loop; infers sequentially until you press "q"
while 1:
    # On "q" keypress, exit
    if cv2.waitKey(1) == ord('q'):
        break

    # Synchronously get a prediction from the Roboflow Infer API
    image = infer()
    # And display the inference results
    cv2.imshow('image', image)

# Release resources when finished
video.release()
cv2.destroyAllWindows()
