# Import the necessary packages 
from imutils import face_utils 
from imutils.video import VideoStream
import imutils 
import dlib
import time 
import cv2 
from playsound import playsound
import numpy as np

# Now, intialize the dlib's face detector model as 'detector' and the landmark predictor model as 'predictor'
print("[INFO]Loading the predictor.....")
detector = dlib.get_frontal_face_detector() 
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')

# Grab the indexes of the facial landamarks for the left and right eye respectively 
(mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Now start the video stream and allow the camera to warm-up
print("[INFO]Loading Camera.....")
vs = VideoStream(src = 0).start()
# Wait for 2 seconds for the camera to get ready
time.sleep(2) 

# Now, loop over all the frames and detect the faces
while True: 
	# Extract a frame 
	frame = vs.read()
	# Resize the frame 
	frame = imutils.resize(frame, width = 500)
	# Convert the frame to grayscale 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Detect faces 
	rects = detector(frame, 1)
	# If a mask is detected, no faces will be detected
	if not rects: 
		cv2.putText(frame, "Mask", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2) 
	# If a face is detected, it means no mask is worn
	else:
		# Now loop over all the face detections and apply the predictor 
		for (i, rect) in enumerate(rects): 
			shape = predictor(gray, rect)
			# Convert it to a (68, 2) size numpy array 
			shape = face_utils.shape_to_np(shape)

			# Draw a rectangle over the detected face 
			(x, y, w, h) = face_utils.rect_to_bb(rect) 
			# Draw a bounding box over the face of the person not wearing a mask
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)	
			cv2.putText(frame, "No Mask", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			# Play any alert sound(Playing sound makes the stream slower, so this is optional)
			# playsound('audio/alarm.mp3')

	# Show the output frame
	cv2.imshow("Output", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the `q` key was pressed, break from the loop
	if key == ord('q'):
		print("[INFO] Ending Video Stream...")
		break

# Do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()