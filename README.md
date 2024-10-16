<<<<<<< Updated upstream
# 2024-ML/AI Prediction Microservices
## Table of Contents
- [ML/AI Prediction Microservices](#2024-MLAIPredictionMicroservices)
  - [Project Overview](#project-overview)
  - [Stakeholders](#stakeholders)
  - [User Stories](#user-stories)
  - [Releases](#releases)
  - [Technologies Used](#technologies-used)
  - [Architecture Diagram](#architecture-diagram)
  - [Flow of Information](#flow-of-information)
  - [Additional Information](#additional-information)
  - [Contributors](#contributors)

## Project Overview
This is a ML/AI microservice top-layer that integrates on an already existing IoT platform for detection of fire, smoke and oil leaks.
=======
<h1>ML/AI Toplayer Microservice</h1>
<h2> Content </h2>
<ul>
  <li><a href="#Project Overview">Projet Overview</a></li>
  <li><a href="#Stake Holders">Stake Holders</a></li>
  <li><a href="#User Stories">User Stories</a></li>
  <li><a href="#Project Structure">Project Structure</a></li>
  <li><a href="#Tech Stack">Tech Stack</a></li>
  <li><a href="#Contributors">Contributors</a></li>
</ul>

<h2 id="Project Overview">Project Overview</h2>
<p>We have been tasked with creating a computer vision solution for a camera-independent anomaly detection system with
two deployment architecture that can work with or without AI edge devices.</p>
>>>>>>> Stashed changes

### Tasks / Features
- We have been tasked with creating a computer vision solution for a camera-independent anomaly detection system
- It will have two deployment architectures that can work with or without AI edge devices.
- The system will provide annomoly detection for oil, fire and smoke with flexibility for future expansion. 
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

## Project Structure

<<<<<<< Updated upstream

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
=======
<h2 id="Stakeholders">Stakeholders</h2>
<ul>
  <li>Dheeraj and team at DigitalU3</li>
</ul>

<h2 id="User Stories">User Stories</h2>
<ul>
  <li>I am a Big corporation A and have many locations with large server rooms, we would like these to be safe whilst not having constant human supervision. We would like to have one service that can <strong>utilise the cameras already in place </strong>at these locations (currently being monitored by staff) to be able to <strong> detect fire or smoke</strong>. We would want cameras to still upload their data to a central server and have the system run on there. Upon detection all managers and duty managers for the respective building should <strong>recieve a text to alert them </strong>of this. Additionally, we would like a <strong>chatbot</strong> that is easy to communicate with to be able to <strong>provide us with analytics and history</strong> for this system.</li>
    <li> I am Big corporation B and I want the same as A, except, I would like to use <strong>AI edge camera devices </strong>instead of the cameras uploading data to the cloud.</li>
</ul>

<h2 id="Project Structure"> Project Structure </h2>

<body>
<ul>
    <li><h3>project/</h3>
        <ul>
            <li><h4>.idea/</h4></li><ul>
            <li>2024-MLAIPredictionMicroservice.iml 
            </li>
            <li>workspace.xml</li>
            </ul>  
            <li><h4>docs/ </h4>  
                <ul>
                    <li>meetings.md
                        <span class="comment"> -------recording all the clients meetings and mentor meetings 
                        </span>
                    </li>
                </ul>
            </li>
            <li><h4>preliminary/ <span class="comment"> -------The folder for the preliminary task
            </span></h4> 
                <ul>
                    <li>dataset/<span class="comment"> -------The dataset that is used for machine learning
                    </span></li>
                    <ul>
                      <li>test/</li>
                      <li>train</li>
                      <li>valid</li>
                      <li>.DS_Store</li>
                    </ul>
                    <li>roboflow-python/</li>
                    <li>.DS_Store</li>
                    <li>infer.py <span class="comment"> -------Object detection that could count number of people in front of the camera</span></li>
                    <li>README.md<span class="comment">            -------details of preliminary task requests<span></li> 
                </ul>
            </li>
            <li>.gitignore</li>
            <li>README.md<span class="comment">            -------overall description of this project<span></li>
        </ul>
    </li>
</ul>

</body>
</html>
</ul>


<h2 id="Tech Stack"> Tech Stack </h2>
<ul>
  <li>Yolo (powered by Ultralytics)
  <li>Roboflow
  <li>Version Control: Git
  <li>
</ul>

<h2 id="Contributors">Contributors </h2>
>>>>>>> Stashed changes

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
| Langauge / Framework | Use |
|:---------------------|:----|
| TBC                  | TBC |

#### Back end

| Langauge / Framework | Use |
|:-- |:--|
|OpenCV| Used to get video stream from camera |
| Roboflow | Train and call feedforward for object detection NN |
|Python| Utilise openCV and roboflow |
| Yolo | Used by roboflow for training NN |

#### Hardware
| Device             | Use                            |
|:-------------------|:-------------------------------|
| Rasberry pi        | Used for testing with a camera |
| AI edge camera TBC | Used for testing AI edge deployment |
| Cloud camera TBC   | Used for testing cloud deployment |

#### Development Tools
| Tool   | Use                                      |
|:-------|:-----------------------------------------|
| Github | Used to manage workloads and share files |

### Experience in Team
| Type                                 | Person/s | Detail |
|:-------------------------------------|:---------|:--|
| Machine Learning and Neural Networks | Tom      | Previous experience training and using neural networks. Researched into optimisation methods.|
| Integrating on top of an existing IoT platform | Will | Done during work experience |
| Python | All | varying degrees of knowledge but all competent |

### Risks
| Project part     | Risk                                                                      |
|:-----------------|:--------------------------------------------------------------------------|
| Object detection | Can lead to catastophe with great fincaical loss and threat to human life |
| SMS/Email alert | Same as above                                                             |


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

## License
Waiting

## Contributors

|      Name      |      Github      |                Link                 |          Email          |
|:--------------:|:----------------:|:-----------------------------------:|:-----------------------:|
|  Thomas Bale   |    tumcuctom     |    https://github.com/TumCucTom     |  hf23482@bristol.ac.uk  |
| Justice Mintah |   justice-123    |   https://github.com/Justice-123    |  ar23247@bristol.ac.uk  |
|   Sin Yi Tay   |     sinyitay     |     https://github.com/SinYiTay     |  if21076@bristol.ac.uk  |
|  William Hook  |   William23292   |   https://github.com/William23292   |  mo23292@bristol.ac.uk  |
|  Xinyaun Chen  | seanchenlovestom | https://github.com/SeanChenLovesTom |  vi23973@bristol.ac.uk  |
| Kanghyeon Kim  |  Kanghyeon5468   |  https://github.com/Kanghyeon5468   |  xx23126@bristol.ac.uk  |
