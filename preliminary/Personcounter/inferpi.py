#for the NN we trained on the dataset that can be found under /dataset
ROBOFLOW_API_KEY = "OQUMCshci7SNfgmSiNDY"
ROBOFLOW_MODEL = "people-counter-mk3"
ROBOFLOW_SIZE = 416

#below needed on my system but unlikely for others
#import sys
#sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')

import cv2
import base64
import numpy as np
import requests


upload_url = "".join([
    "https://detect.roboflow.com/",
    ROBOFLOW_MODEL,
    "?access_token=",
    ROBOFLOW_API_KEY,
    "&format=image",
    "&stroke=5"
])

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("could not open camera")
    exit(1)

import cv2
import io
import numpy as np
import requests

ROBOFLOW_API_KEY = "OQUMCshci7SNfgmSiNDY"
ROBOFLOW_MODEL = "people-counter-mk3"
ROBOFLOW_VERSION = "1"  # Add your model version here
ROBOFLOW_SIZE = 416

upload_url = f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}?api_key={ROBOFLOW_API_KEY}&format=image&stroke=5"

def infer():
    ret, img = video.read()
    if not ret:
        print("Failed to capture image")
        return None
    print("Image captured successfully")

    try:
        # Resize the image
        height, width, channels = img.shape
        scale = ROBOFLOW_SIZE / max(height, width)
        img = cv2.resize(img, (round(scale * width), round(scale * height)))
        print(f"Resized image dimensions: {img.shape}")
    except Exception as e:
        print(f"Error when resizing image: {e}")
        return None

    try:
        # Encode image to JPEG
        retval, buffer = cv2.imencode('.jpg', img)
        if not retval:
            print("Failed to encode image")
            return None
        img_bytes = io.BytesIO(buffer)

        # Prepare the files payload
        files = {
            'file': ('image.jpg', img_bytes, 'image/jpeg')
        }

        # Get prediction from Roboflow Infer API
        response = requests.post(upload_url, files=files, stream=True)
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
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if image is None:
            print("Failed to decode image from API response")
            return None
        print(f"Processed image dimensions: {image.shape}")
    except Exception as e:
        print(f"Error when parsing result image: {e}")
        return None

    return image
 


# Main loop; infers sequentially until you press "q"
while 1:
    # On "q" keypress, exit
    if(cv2.waitKey(1) == ord('q')):
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