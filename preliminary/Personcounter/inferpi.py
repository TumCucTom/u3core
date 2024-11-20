"""Infer for a raspberry pi"""
import sys
import io
import cv2
import numpy as np
import requests

ROBOFLOW_API_KEY = "OQUMCshci7SNfgmSiNDY"
ROBOFLOW_MODEL = "people-counter-mk3"
ROBOFLOW_VERSION = "1"  # Add your model version here
ROBOFLOW_SIZE = 416

#below needed on my system but unlikely for others
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')


UPLOAD_URL = (f"https://detect.roboflow.com/"
              f"{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}?"
              f"api_key={ROBOFLOW_API_KEY}&format=image&stroke=5")

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("could not open camera")
    sys.exit()

def infer():
    """Process the images and utilise roboflow model"""
    ret, img = video.read()
    if not ret:
        print("Failed to capture image")
        return None
    print("Image captured successfully")

    try:
        # Resize the image
        height, width, _ = img.shape
        scale = ROBOFLOW_SIZE / max(height, width)
        img = cv2.resize(img, (round(scale * width), round(scale * height)))
        print(f"Resized image dimensions: {img.shape}")
    except Exception as e:
        print(f"Error when resizing image: {e}")
        return None

    try:
        # Encode image to JPEG
        ret_val, buffer = cv2.imencode('.jpg', img)
        if not ret_val:
            print("Failed to encode image")
            return None
        img_bytes = io.BytesIO(buffer)

        # Prepare the files payload
        files = {
            'file': ('image.jpg', img_bytes, 'image/jpeg')
        }

        # Get prediction from Roboflow Infer API
        response = requests.post(UPLOAD_URL, files=files, stream=True,timeout=5.0)
        if response.status_code != 200:
            print(f"API returned an error: {response.status_code} {response.text}")
            return None
        resp = response.raw
    except Exception as e:
        print(f"Error when calling Roboflow: {e}")
        return None

    try:
        # Parse result image
        data = resp.read()
        if not data:
            print("Received empty response from API")
            return None
        new_image = np.asarray(bytearray(data), dtype="uint8")
        new_image = cv2.imdecode(new_image, cv2.IMREAD_COLOR)
        if new_image is None:
            print("Failed to decode image from API response")
            return None
        print(f"Processed image dimensions: {new_image.shape}")
    except Exception as e:
        print(f"Error when parsing result image: {e}")
        return None

    return image

# Main loop; infers sequentially until you press "q"
while 1:
    # On "q" keypress, exit
    if cv2.waitKey(1) == ord('q'):
        break

    # Synchronously get a prediction from the Roboflow Infer API
    image = infer()
    if image is not None:
        # And display the inference results
        cv2.imshow('image', image)
    else:
        print("no image to display")

# Release resources when finished
video.release()
cv2.destroyAllWindows()
