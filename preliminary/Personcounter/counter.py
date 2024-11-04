from roboflow import Roboflow
import cv2

rf = Roboflow(api_key="FRUmKXAzM8M7TupHxPph")
project = rf.workspace().project("person-counter-6kxom")
model = project.version(2).model

#change input number from 0 to change the camera in use
video = cv2.VideoCapture(0)

# Use roboflow to get the JSON with predictions from the NN
def count():
    # Get the current image from the webcam
    ret, img = video.read()

    # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
    height, width, channels = img.shape
    scale = ROBOFLOW_SIZE / max(height, width)
    img = cv2.resize(img, (round(scale * width), round(scale * height)))

    # infer on a local image
    print("Number of people: ", len(model.predict(img, confidence=40, overlap=30).json()['predictions']))

# Main loop; infers sequentially until you press "q"
while 1:
    # On "q" keypress, exit
    if(cv2.waitKey(1) == ord('q')):
        break

    # Synchronously get a prediction from the Roboflow Infer API
    image = count()


# Release resources when finished
video.release()
cv2.destroyAllWindows()
