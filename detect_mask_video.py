# Import the necessary dependencies
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from playsound import playsound
import numpy as np
import imutils
import time
import cv2
import os

# Create a function to detect faces from an image and return the coordinates of the bounding box and the perdiction score
def detect_and_predict_mask(frame, faceNet, maskNet):
	# Grab the dimensions of the frame and then construct a blob from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))

	# Pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# Initialize our list of faces, their corresponding locations, and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# Loop over the detections
	for i in range(0, detections.shape[2]):
		# Extract the confidence (i.e., probability) associated with the detection
		confidence = detections[0, 0, i, 2]

		# Filter out weak detections by ensuring the confidence is greater than the minimum confidence
		if confidence > 0.5:
			# Compute the (x, y)-coordinates of the bounding box for the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Ensure the bounding boxes fall within the dimensions of the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# Extract the face ROI, convert it from BGR to RGB channel ordering, resize it to 224 x 224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# Add the face and bounding boxes to their respective lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# Only make a predictions if at least one face was detected
	if len(faces) > 0:
		# For faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions in the above `for` loop
		faces = np.array(faces, dtype = "float32")
		preds = maskNet.predict(faces, batch_size = 32)

	# Return a 2-tuple of the face locations and their corresponding locations
	return (locs, preds)

# Load our serialized face detector model from disk
prototxtPath = r"models\deploy.prototxt"
weightsPath = r"models\res10_300x300_ssd_iter_140000.caffemodel"
# Get the facenet ready
faceNet = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)

# Load the face mask detector model that has been trained, from disk
maskNet = load_model("models/mask_detector.model")

# Initialize the video stream
print("[INFO] Starting Video Stream...")
vs = VideoStream(src = 0).start()
# Wait for 2 seconds for the camera to get ready
time.sleep(2)

# Loop over the frames from the video stream
while True:
	# Grab the frame from the threaded video stream and resize it to have a maximum width of 600 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width = 600)

	# Detect faces in the frame and determine if they are wearing a face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# Loop over the detected face locations and their corresponding locations
	for (box, pred) in zip(locs, preds):
		# Unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred

		# Determine the class label and color we'll use to draw the bounding box and text
		label = "Mask" if mask > withoutMask else "No Mask"
		if label == "Mask":
			color = (0, 255, 0) 
		else:
			color = (0, 0, 255)
			# Play any alert sound(Playing sound makes the stream slower, so this is optional)
			# playsound('audio/alarm.mp3')

		# Include the probability in the label
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		# Display the label and bounding box rectangle on the output frame
		cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

	# Show the output frame
	cv2.imshow("Output", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the `q` key was pressed, break from the loop
	if key == ord("q"):
		print("[INFO] Ending Video Stream...")
		break

# Do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()