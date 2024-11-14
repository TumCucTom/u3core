#below needed on my system but unlikely for others
#import sys
#sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')

import base64
import cv2

#size of the image you want to send to the network in SIZE x SIZE pixels
SIZE = 416

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)

# Get and preprocess a frame
def get_Image():
    # Get the current image from the webcam
    ret, img = video.read()
    if img is None:
        print("Failed to capture image")
        return None

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, channels = img.shape
    scale = SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # Encode image to base64 string
    retval, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)


# Release resources when finished
video.release()
cv2.destroyAllWindows()