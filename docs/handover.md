# State of the project

In any main section of the repo, you should find a README that provides information on what that section does and how to work on it

## Backend

### Server

- This can be found under ```code/backend/python-server```
- This contains:
  - server.py - The main entry point for the backend, registers all the endpoints and initialises the server
  -database.py - database.py - Manages database connections and table initialisation
  - fire_detection.py -  Contains functions for running fire detection on RTSP streams
  - email_utils.py - Provides utilities for sending emails via Postmark API
  - fire_detection_script.py - Holds the implementation of fire detection
  - Endpoints directory - Contains modularised api endpoint handlers
    -init.py - Package initialisation, exports all api registration functions
    -endpoint_utils.py - Shared utility functions for endpoints (such as table counting)
    -camera_endpoints.py - Endpoints for camera management (add, update, delete, get count)
    -site_endpoints.py - Endpoints for site management (add, update, delete, fetch, get count)
    -hazard_endpoints.py - Endpoints for hazard logging and retrieval
    -analytics_endpoints.py - Endpoints for analytics data (anomalies by month, by type, for dashboard)
    -user_endpoints.py - Endpoints for user authentication and management
    
  - A copy of yolov8 to be used for training user models
  - A datasets directory that holds user's datasets they've uploaded for training
- You run this on AWS: done automatically on github with an action
- OR you can do manually with:
  - ```cd code/backend```
  - ```docker compose --env-file ../../../.env up --build -d```
- Once you've got docker and docker compose installed and working

### Docker compose

You can find docker compose file at ```code/backend/docker-compose.yml```
This sets up the environment, how containers interact and runs the database.

The ```Dockerfile.xx``` run the parts of the backend. The only relevant one currently is the backend which runs the python server
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
### AWS
- The server being used for the backend is the u3CoreServer instance.
- This is a t2-small instance with a 100GB volume attached

### Github
- Github action workflows can be found under ```.github/workflows```
- Two other contributors must approve a PR before it is pulled into dev
