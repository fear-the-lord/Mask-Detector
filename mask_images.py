# Import the necessary dependencies
import dlib
from PIL import Image
import argparse
from imutils import face_utils
import numpy as np
import moviepy.editor as mpy
import os

print("[INFO]Loading Shape Predictor.....")
# Load the dlib face detector
detector = dlib.get_frontal_face_detector()
# Load the dlib shape predictor
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')

# Resize to a max_width to keep jpg size small
max_width = 500

# Count the number of images in the dataset
list = os.listdir("dataset/without_mask")
number_files = len(list)

# Loop over all the images in the dataset
for i in range(0, number_files - 1):
    input_image_path = "dataset/without_mask/img" + str(i) + ".jpg"
    print("[INFO] Processing image " + input_image_path)
    # Open our image, convert to RGBA
    img = Image.open(input_image_path).convert('RGBA')

    # Open the image of the mask
    mask = Image.open("images/mask.png")

    # Scale the image
    if img.size[0] > max_width:
        scaled_height = int(max_width * img.size[1] / img.size[0])
        img.thumbnail((max_width, scaled_height))

    # Convert the image to grayscale
    img_gray = np.array(img.convert('L'))
    # Detect the faces
    rects = detector(img_gray, 0)

    # If no faces are found
    if len(rects) == 0:
        print("[INFO] No faces found...")

    # If a face is found
    print("[INFO] %i faces found in source image. processing into jpg now..." % len(rects))

    faces = []
    # Loop over all the faces detected
    for rect in rects:
        face = {}
        # Print the dimesnions of the bounding box
        print(rect.top(), rect.right(), rect.bottom(), rect.left())
        # Fit the mask size as per the size of the mouth
        mask_width = rect.right() - rect.left()
        mask_width += 50

        # Predictor used to detect orientation in place where current face is
        shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Grab the outline of the mouth
        mouth = shape[49:68]
        # Compute the center of mass for the mouth
        mouthCenter = mouth.mean(axis = 0).astype("int")

        # Resize the mask image to fit face width
        current_mask = mask.resize((mask_width, int(mask_width * mask.size[1] / mask.size[0])), resample = Image.LANCZOS)

        # Add the scaled image to a list, and adjust the mask on the mouth
        face['mask_image'] = current_mask
        mouth_x = mouth[0,0] - mask_width // 4
        mouth_x -= 20
        mouth_y = mouth[0,1] - mask_width // 6
        mouth_y -= 20
        face['final_pos'] = (mouth_x, mouth_y)
        faces.append(face)

    # Convert the images back to RGB
    draw_img = img.convert('RGB')
    draw_img.paste(face['mask_image'], face['final_pos'], face['mask_image'])
    # Store the images on the new folder
    final_image_path = "dataset/with_mask/final" + str(i) + ".jpg"
    draw_img = draw_img.save(final_image_path)

print("[INFO] Images Masked Successfully...")
print("[INFO] Press BACK Button...")