# State of the project

## Backend

### Server

- This can be found under ```code/backend/python-server```
- This contains:
  - server.py - this holds the api endpoints that get called by the website
    - It also starts fire detection on all stored rtsp addresses
  - fire_detection_script.py - holds the implementation of fire detection
  - A copy of yolov8 to be used for training user models
  - A datasets directory that holds user's datasets they've uploaded for training
- You run this on AWS: done automatically on github with an action
- OR you can do manually with:
  - ```cd code/backend```
  - ```docker compose --env-file ../../../.env up --build -d```
- Once you've got docker and docker compose installed and working

## Frontend
- This a quasar webapp
- This use vue.js scripts
- You can run a local dev version of this by:
  - ```cd code/frontend```
  - ```npm run dev```
- You can deploy this with
  - ```cd code/frontend```
  - ``` quasar build```
  - Then put the files under spa/dist in the blue host
  - NOTE: This is done on github actions to www.ai.u3core.com using FTP

## Other

## What's to do?

## Backend
LATER

## Frontend
LATER
## Other
LATER