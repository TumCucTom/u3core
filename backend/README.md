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
