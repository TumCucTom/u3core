![Roboflow](https://img.shields.io/badge/roboflow-6706CE?style=for-the-badge&logo=roboflow&logoColor=#6706CE)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) 
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) 
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) 
![AWS](https://img.shields.io/badge/aws-%23232f3e.svg?style=for-the-badge&logo=amazon-web-services&logoColor=white) 

# 2024-ML/AI Prediction Microservices
## Table of Contents
- [2024-ML/AI Prediction Microservices](#2024-mlai-prediction-microservices)
  - [Project Overview & structure](#project-overview)
  - [User/ Developer Instructions](#user-instructions)
  - [Stakeholders and User stories](#stakeholders)
  - [Releases and Technologies](#releases)
    - [Tech Stack Analysis](#tech-stack-analysis)
    - [Experience in Team](#experience-in-team)
    - [Risks](#risks)
  - [Architecture and Information](#architecture-diagram)
  - [License and Contributors](#license)

## Project Overview
This is a ML/AI microservice top-layer that integrates on an already existing IoT platform for detection of fire, smoke and oil leaks.

### Tasks / Features

#### Frontend
- There should be Email ID setup and an authentication workflow
- User friendly UI
- UI integration with the backend 
- Camera and device integration

#### Backend
- We have been tasked with creating a computer vision solution for a camera-independent anomaly detection system
- It will have two deployment architectures that can work with or without AI edge devices.
- The system will provide anomaly detection for oil, fire and smoke with flexibility for future expansion. 
- It will have support for AI edge devices and cloud deployment and be scalable for multi-site deployments.
- It will have a simple alarm console to receive and track detected anomalies with the ability to configure alarms via Email, SMS, and WhatsApp for relevant users.
- It will have basic reporting functionality to track incidents and export logs must also be included.
- It will integrate with a variety of camera makes/models.
- APIs of the solution will be made available to be able to integrate with any 3rd part alarms,bms, analytics systems.
- It should have an natural language AI that can relay information about the system and the history of the system

### Project Links
- [**Kanban Board**](https://github.com/orgs/spe-uob/projects/237)
- [**Milestones**](https://github.com/spe-uob/2024-MLAIPredictionMicroservices/milestones)
- [**Issues**](https://github.com/spe-uob/2024-MLAIPredictionMicroservices/issues)
- [**Pull Requests**](https://github.com/spe-uob/2024-MLAIPredictionMicroservices/pulls)
- [**Gnatt Chart/Roadmap**](https://github.com/orgs/spe-uob/projects/237/views/4)

## Project Structure
```
📁 project/
├── 📁 .idea/
│    ├──📄 2024-MLAIPredictionMicroservice.iml
│    └──📄 workspace.xml
├── 📁 alert system/
│    └──📄 alert_sys.py
│        └── ------ Building up alert system
├── 📁 docs/
│    ├──📄 ethics.md
│    └──📄 meetings.md
│        └── ------- Recording all the clients meetings and mentor meetings
├──📁 preliminary/
│   ├──📁 Personcounter/
│   │    ├──📁 dataset/
│   │    │   ├──------- The dataset that is used for machine learning
│   │    │   ├──📁 test/
│   │    │   ├──📁 train/
│   │    │   └──📁 valid/
│   │    ├──📁 roboflow-python/
│   │    └──📄 infer.py
│   │        └── ------- Object detection that could count number │of people in front of the camera
│   └──📄 README.md
│       └── ------- Details of preliminary task requests
├──📄 .gitignore
└──📄 README.md
    └── ------- Overall description of the project
```

## User Instructions

## Developer Instructions

## Stakeholders
### DigitalU3
- Delivered their needs and wants to use
- Aims to sell and deploy this system to corporations via the cloud and on AI edge devices
- Aims to help corporations keep unmanned spaces safe

### Unnamed client
- Providing the training data
- More info to come

## User stories
- As a **team at DigitalU3**, we want the system to be able to be deployed seamlessly on either AI edge or cloud devices. 
- As a **team at DigitalU3**, we want the SMS/email alert system to be easily setup.
- As a **manager at unnamed corporation**, I want the SMS alerts to arrive at my phone fast and securely.
- As a **manager at unnamed corporation**, I want the detection alerts to detect hazards before they have caused significant damage

## Releases

## Technologies Used
### Tech Stack Analysis
INSERT DIAGRAM HERE
#### Front end
| Langauge / Framework | Use                                                                 |
|:---------------------|:--------------------------------------------------------------------|
| Figma                | Designs for UI (user registration, camera setup, alerts management) |
| AWS | To integrate with backend |
| React/Angular | Build front end |

#### Back end

| Langauge / Framework | Use |
|:---------------------|:--|
| OpenCV               | Used to get video stream from camera |
| Roboflow             | Train and call feedforward for object detection NN |
| Python               | Utilise openCV and roboflow |
| Yolo                 | Used by roboflow for training NN |
| Twilio               | Used for the alert system |
| AWS SNS | Used for alert system |
| RTSP | To send video footage over web |

#### Hardware
| Device                       | Use                            |
|:-----------------------------|:-------------------------------|
| Rasberry pi                  | Used for testing with a camera |
| AI edge camera (Intel-based) | Used for testing AI edge deployment |
| Cloud camera TBC             | Used for testing cloud deployment |

#### Development Tools
| Tool   | Use                                      |
|:-------|:-----------------------------------------|
| Github | Used to manage workloads and share files |

### Experience in Team
| Type                                 | Person/s | Detail                                                                                        |
|:-------------------------------------|:---------|:----------------------------------------------------------------------------------------------|
| Machine Learning and Neural Networks | Tom      | Previous experience training and using neural networks. Researched into optimisation methods. |
| Integrating on top of an existing IoT platform | Will | Done during work experience                                                                   |
| Python | All | Varying degrees of knowledge but all competent                                                |

### Risks
| Project part     | Risk                                                                      |
|:-----------------|:--------------------------------------------------------------------------|
| Object detection | Can lead to catastophe with great fincaical loss and threat to human life |
| SMS/Email alert | Can lead to catastophe with great fincaical loss and threat to human life                                                            |


## Architecture Diagram

INSERT DIAGRAM HERE

|          **Component**          |                                        **Description**                                         |
|:-------------------------------:|:----------------------------------------------------------------------------------------------:|
|       **AI edge Camera**        |                    Captures video of current environment and runs all code                     |
|        **Cloud Camera**         |                       Video capture via openCV and uploads to the cloud                        |
|           **SMS API**           |                Send a given message to the store phone numbers/email addresses                 |
|   **Roboflow trained model**    |                     Holds all of the nodes and biases of the trained model                     |
| **Roboflow feed-forwards pass** |            One pass of the input data through the network giving prediction results            |
|        **Roboflow API**         | Takes input data for the network and runs a feedforward remotely, returning prediction results 
|       **multinodal LLM**        |          Takes natural language as input and outputs: system data or natural language          |  

## Flow of Information
### AI Edge
1. **AI edge camera** captures video of the environment it is in.
2. **AI edge Camera** does image pre processing to make the current image of the correct format for the NN.
3. **AI edge camera** uses **Roboflow trained model** stored on the camera and will take the input data and undergo one **feed-forward pass**.
4. **AI edge camera** if the model makes a prediction above the given threshold:
   1. **AI edge camera** sends SMS/Email via **API to be chosen**.

### Cloud system
1. **Cloud Camera** captures video of the environment it is in.
2. **Cloud Camera** sends the image to a central system.
3. Central system does image pre-processing to make the current image of the correct format for the NN.
4. Central system calls **Roboflow API** and receives the prediction in response.
5. If the model makes a prediction above the given threshold:
  1.  Central system send SMS/Email via **API to be chosen**.

### At any time
1. A user can use the **chat bot**
   1. The text input is given to the **mulitnodal LLM**
   2. It returns to the user either data about the system or a text response.

## Additional Information
### Testing
| Test | How it is tested |
|:- | :- |
|Test system with actual video feeds (oil, smoke, fire) ||
|Full backend & frontend integration||
|AWS deployment for cloud-based anomaly detection system||

## License
[type of license](LICENSE.md)

## Contributors

### Names and information

|      Name      |      Github      |                Link                 |          Email          |
|:--------------:|:----------------:|:-----------------------------------:|:-----------------------:|
|  Thomas Bale   |    tumcuctom     |    https://github.com/TumCucTom     |  hf23482@bristol.ac.uk  |
| Justice Mintah |   justice-123    |   https://github.com/Justice-123    |  ar23247@bristol.ac.uk  |
|   Sin Yi Tay   |     sinyitay     |     https://github.com/SinYiTay     |  if21076@bristol.ac.uk  |
|  William Hook  |   William23292   |   https://github.com/William23292   |  mo23292@bristol.ac.uk  |
|  Xinyaun Chen  | seanchenlovestom | https://github.com/SeanChenLovesTom |  vi23973@bristol.ac.uk  |
| Kanghyeon Kim  |  Kanghyeon5468   |  https://github.com/Kanghyeon5468   |  xx23126@bristol.ac.uk  |

### Responsbilities

| Frontend | Backend | Full stack |
|:-: |:-:| :-: |
|William | Kanghyeon | Thomas |
|Sin Yi | Xinyuan | Justice |

- Client Liason: Justice
- Mentor Liason: Thomas

