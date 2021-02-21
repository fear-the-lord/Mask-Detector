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

My model gives an accuracy of about 96% on the training set and about 98% on the validation set. So I consider it a pretty decent model for mask detection. 
The graph of loss vs accuracy on both training and test data looks like: 
![plot](https://user-images.githubusercontent.com/35571958/108630831-e9b30880-748c-11eb-93d6-3160882f8c21.png)
