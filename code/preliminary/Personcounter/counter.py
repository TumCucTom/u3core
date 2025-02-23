"""Count the number of people in a room"""
from roboflow import Roboflow
import cv2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ROBOFLOW_SIZE = 416
API_KEY = os.getenv('API')
rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project("person-counter-6kxom")
model = project.version(2).model

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)

def count():
    """ Use roboflow to get the JSON with predictions from the NN"""
    # Get the current image from the webcam
    _, img = video.read()

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, _ = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # infer on a local image
    num_predictions = len(model.predict(img, confidence=40, overlap=30).json()['predictions'])
    print("Number of people: ", num_predictions )

# Main loop; infers sequentially until you press "q"
while 1:
    # On "q" keypress, exit
    if cv2.waitKey(1) == ord('q'):
        break

    # Synchronously get a prediction from the Roboflow Infer API
    count()


# Release resources when finished
video.release()
cv2.destroyAllWindows()
