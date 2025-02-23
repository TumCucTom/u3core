## Working pipeline
### On start
- Docker will connect the database to the main server
- The main server upon launch will get all stored RTSP addresses from the database
- Upon retrieving, it will concurrently run hazard detection on all the RTSP addresses:
  - This is done by calling the detection script with the RTSP address
  - Each frame is taken and processed by openCV
  - We pre-process the frame ready to 
  - RESTfuly roboflow for predictions on the frame
  - If a prediction is detected we call a hazard logging endpoint in the main server

### Endpoints
We have endpoints for:
- Adding new cameras and sites
- Adding new users and async encryption fo their sensitive information
- Retrieving DB information inc hazard detection and user info
- Starting a new fire detection process

## Testing Pipeline
- RTSP server runs on amazon ec2 instance using [mediamtx](https://github.com/bluenviron/mediamtx/tree/main)
    - It uses TCP
    - Port forwarding rules must be adjusted on the ec2 instance
- We write to the stream using OBS with computer webcam
- A different machine can read from the stream using openCV
    - The RTSP URL is taken as the camera input
- The roboflow API is called with the current frame
- It returns a JSON including any predictions
- If a prediction is given, an alert is sent to a given number
    - This is on whatsapp via Twilio

## Testing RTSP

- We use [mediamtx](https://github.com/bluenviron/mediamtx/tree/main) to test rtsp streaming in conjunction with obs studio
- You can see instructions on how to setup this process in [Dev Instructions](../../README.md#developer-instructions).
- We can use our webcam in OBS studio and send the data to the rtsp server hosted locally by mediamtx
- We can then take from this stream using openCV in python or output to a file using ffmpeg
