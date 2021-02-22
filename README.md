# Mask Detection System

<img src="https://img.shields.io/github/repo-size/fear-the-lord/Mask-Detector"> <img src="https://img.shields.io/github/license/fear-the-lord/Mask-Detector"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/fear-the-lord/Mask-Detector"> <img src = "https://hitcounter.pythonanywhere.com/count/tag.svg?url=https://github.com/fear-the-lord/Mask-Detector"> <img src = "https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen">

## Motivation
This system has been developed, keeping in mind, the current pandemic situation. In order to detect if a person entering any building has put his/her mask on, 
an efficient system needs to be designed, where it can detect and raise an alarm, in real time, if a person is not wearing a mask. 

## Running the System

### Step 1: Clone the repository into the system
```bash
git clone https://github.com/fear-the-lord/Mask-Detector.git
```
or directly download the file as zip and extract

### Step 2: Install the dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the index file
```bash
python index.py
```

## System Details
This system is works in two different ways: 
1. Mask Detection using Imagenet.
2. Mask Detection using Dlib. 

This system works in two different ways to provide the same result but with different accuracy. 
In my case, the system designed using Dlib provides better accuracy than the system designed using Imagenet. 

I have tried to keep the user intervention as less as possible while designing the system.
The user will have two options to choose(mentioned above). 

If the user chooses option 1, then there are a few steps to follow: 
1. The dataset needs to be created, for this, I have used selenium, to scrap through the web and download images automatically. 
2. Then all the images downloaded will be masked automatically using Face Detector and a separate dataset will be created. 
3. After that the training will take place and a model will be created. 
4. This model will be used to detect masks. 

NOTE: After downloading the images, the user needs to go through the images ones and delete all the images which doesnot contain a face, or the images in which 
the mask has not been placed correctly. This is an optional step, the user might not do it, but doing this ensures better accuracy. 

My model gives an accuracy of about 96% on the training set and about 98% on the validation set. So, I consider it a pretty decent model for mask detection. 
The graph of Loss vs. Accuracy on both training and test data looks like: 
![plot](https://user-images.githubusercontent.com/35571958/108630831-e9b30880-748c-11eb-93d6-3160882f8c21.png)

Now, coming to the 2nd part, where I have worked with Dlib. This system is much more accurate and easy to understand. 
The number of lines of code are pretty less. It's working is pretty simple, I have used the facial landmarks detector of dlib, 
to detect the mouth. If the mouth is detected it means that the person is not wearing a mask.

## Streaming using Phone Camera 
We have used and Android App available for free in Play Store, named IP Webcam. It can be downloaded from this <a href = "https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN">link</a>. After downloading it, open the app and scroll down to the option <b>Start Server</b>. It will look like: <br>
<img src = "https://user-images.githubusercontent.com/35571958/88623867-83673280-d0c3-11ea-9efd-63559024c0bd.jpg">

After starting the server, an IP will be displayed on the screen. Open the file <b>android_cam.py</b>. In <b>line 36</b> put the given IP. 
```python
url = "http://<YOUR_IP_HERE>/shot.jpg"
```
<b>Also, make sure that the phone and PC/Laptop is connected to the same network.</b>

Also, in order to toggle between the front and back camera, type the IP upto "http://<YOUR_IP_HERE>" in the search bar of yor browser and explore the page which will look like this: <br>
<img src = "https://user-images.githubusercontent.com/35571958/88626505-5f5a2000-d0c8-11ea-88f0-e1d4481eb9d9.png">

## Future Scope
Looking forward to convert it to a mobile app, also looking to add more features like: Cough Detection, Sneeze Detection. 

## References
[1]Eye blink detection with OpenCV, Python, and dlib: https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
[2]MobileNet and MobileNetV2: https://keras.io/api/applications/mobilenet/
