## Backend
This contains files / directories related to:
- Docker:
   - Running all backend together
- Server:
  - Actual python backend server
  - Holds API endpoints
  - Runs the NN
- Test scripts:
  - Scripts used to test features before putting in server
- Websocket server:
  - For RTSP streaming
### Structure

```angular2html
├── backend                            # Backend-related services and scripts
│   │   ├── Dockerfile.backend         # Docker configuration for the backend server
│   │   ├── Dockerfile.websocket       # Docker configuration for the websocket service
│   │   ├── README.md                  # Overview of the backend setup
│   │   ├── db                         #
│   │   │   ├── Dockerfile             # Docker configuration for the database
│   │   │   └── custom-shutdown.sh     # Custom script for database shutdown to preserve its state
│   │   ├── docker-compose.yml         # Docker Compose setup for backend services
│   │   ├── initdb                     #
│   │   │   ├── README.md              # Overview of database initialization
│   │   │   └── dump.sql               # SQL dump for initial database setup
│   │   ├── python-features            #
│   │   │   ├── alert_sys.py           # Script for alert system implementation
│   │   │   ├── full_interation.py     # Script with all features integrated
│   │   │   └── image_get_prep.py      # Script for image preprocessing only
│   │   ├── python-server              # Backend server
│   │   ├── requirements.txt           # Python dependencies for the backend
│   │   ├── training                   #
│   │   │   └── README.md              # Overview of training techniques and performance
│   │   └── websocket-server           # Websocket server
```

## Frontend

This contains a frontend web app build with vue scripts using quasar.js.

### Structure
```angular2html
├── frontend                       
│   │   ├── README.md                  # Overview of the frontend setup
│   │   └── web-app                    # Frontend quasar web application
```

## Preliminary

All preliminary scripts for gaining relevant knowledge for this application

### Structure
```
preliminary                    # Early-stage experimental code and prototypes
│       ├── Personcounter              #
│       │   ├── counter.py             # Person counting NN
│       │   ├── infer.py               # NN for people detection
│       │   └── inferpi.py             # Raspberry Pi-specific for above
│       └── README.md                  # Overview of preliminary code

```