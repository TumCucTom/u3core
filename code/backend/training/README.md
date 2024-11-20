# Training Data

## Collecting

### Fire
- We searched the web on many open source sites and through research papers
- Many of the papers create their own dataset by handpicking images which we deemed was not worth our time for the preliminary testing
- Many of the datasets on kaggle and robolow universe are not annotated and so we did not use them, again due to time constraints
- We found this repo: https://github.com/robmarkcole/fire-detection-from-images
    - Which uses this dataset https://github.com/OlafenwaMoses/FireNET?tab=readme-ov-file
    - This contained 482 images

### Oil
- This was given to us by the client
- 3 datasets were given:
    - Chemical spills
    - General liquids
    - Oil spillages
- We have no further information on how the dataset was obtained

## Preprocessing and augmentation

### Fire

| Name | Number | Preprocessing | Augmentation | Label Format |
|:-:|:-:|:-:|:-:| :-:|
| FireNet| 482 | None | None | YOLOv3 Format |
| Our modified FireNet | 1162 | * Resize to 640x640 (Stretch) | * Shear: 10 degress horizontal and vertical. This is to try and account for camera lens distortion for wide lenses<br/> * Hue: 15% for different colours of fire (possibly caused by chemicals or changes in lighting conditions<br/> * Blur: 1px for if the fire is out of focus | YOLOv3 Format |
| Updated, modified FireNet for combined | 1162 | * Auto-orientation of pixel data (with EXIF-orientation stripping) <br/> * Resize to 640x640 (Stretch) | * Shear: 10 degress horizontal and vertical. This is to try and account for camera lens distortion for wide lenses<br/> * Hue: 15% for different colours of fire (possibly caused by chemicals or changes in lighting conditions<br/> * Blur: 1px for if the fire is out of focus | YOLOv8 Format |


### Oil

|      Name       | Number | Preprocessing                                                                                          |                                                                                                                   Augmentation                                                                                                                   | Label format |
|:---------------:|:------:|:-------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:| :-: |
| Chemical Spill  |  2093  | * Auto-orientation of pixel data (with EXIF-orientation stripping) <br/> * Resize to 640x640 (Stretch)                                                                                                       |                                                                                                                       None                                                                                                                       |YOLOv8 format|
| General Liquids |  1086  | * Auto-orientation of pixel data (with EXIF-orientation stripping) <br/> * Resize to 640x640 (Stretch) | * 50% probability of horizontal flip<br/>* 50% probability of vertical flip<br/>* Random rotation of between -15 and +15 degrees<br/>* Random exposure adjustment of between -10 and +10 percent  <br/> <br/> Creating 3 versions of each image  |YOLOv8 format|
|  Oil Spillage   |  2972  | * Auto-orientation of pixel data (with EXIF-orientation stripping)                                     |                                                                                                                       None                                                                                                                       |YOLOv8 format|

## Training and Results:
#### Fire
These images were then first trained with yolov11 with the MSCOCO starting point given by roboflow. See below for details:

<img width="600" alt="image" src="https://github.com/user-attachments/assets/3b1be7f1-1796-48c1-ad0e-c4412cefa1a9">
<img width="600" alt="image" src="https://github.com/user-attachments/assets/2e46808d-d06e-462b-9418-cdfda09c3f21">

As you can see above, the initial training from this dataset is relatively good.


### Oil
These images were then first trained with yolov11 with the MSCOCO starting point given by roboflow. See below for details:

| Test | Valid|
|:-:|:-:
|<img width="350" alt="image" src="https://github.com/user-attachments/assets/b2ef593e-550b-49ed-9e2c-5cd1fd450377">|<img width="350" alt="image" src="https://github.com/user-attachments/assets/4754b70f-13c7-43e6-a971-281f55af755b">|

<img width="600" alt="image" src="https://github.com/user-attachments/assets/943867f6-bb99-471c-980a-4336d0d23322">
<img width="600" alt="image" src="https://github.com/user-attachments/assets/4184a71f-5a92-4ad2-a906-8b08237c583d">


As you can see above, the initial training from this dataset is poor.


#### Combined
These images were then first trained with yolov11 with the MSCOCO starting point given by roboflow. See below for details:

| Test | Valid|
|:-:|:-:|
|<img width="350" alt="image" src="https://github.com/user-attachments/assets/ce353e46-c5da-4721-8e8f-e197e52d1959">|<img width="350" alt="image" src="https://github.com/user-attachments/assets/9b721384-b176-444b-85f0-e275705856c3">|

<img width="600" alt="image" src="https://github.com/user-attachments/assets/ab4c603f-5e1b-40b0-98fc-0bc214078469">
<img width="600" alt="image" src="https://github.com/user-attachments/assets/591c2fab-1713-4ae0-a3c9-f46b1fd8e98a">


The results are inbetween oil and fire as expected. Improvements to come...

