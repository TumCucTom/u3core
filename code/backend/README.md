## Process (so far)
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

## Training Data
Find infomation about training data in the [Training README](training/README.md)

## Image Preprocessing

- OpenCV is used to get camera video stream from rtsp
- OpenCV is used to preprocess the the frames

## RTSP

- We use [mediamtx](https://github.com/bluenviron/mediamtx/tree/main) to test rtsp streaming in conjunction with obs studio
- You can see instructions on how to setup this process in [Dev Instructions](README.md#developer-instructions).
- We can use our webcam in OBS studio and send the data to the rtsp server hosted locally by mediamtx
- We can then take from this stream using openCV in python or output to a file using ffmpeg

## Web Server
- Handles SQL calls to the user database
- Performs async encryption for passwords
