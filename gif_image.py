import dlib
from PIL import Image
import argparse
from imutils import face_utils
import numpy as np
import moviepy.editor as mpy

# parser = argparse.ArgumentParser()
# parser.add_argument("-image", required = True, help = "path to input image")
# args = parser.parse_args()

print("[LOADING]Shape predictor.....")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# resize to a max_width to keep jpg size small
max_width = 500

n = input("Enter the number of images: ")
n = int(n)

for i in range(0, n):
    input_image_path = "dataset/without_mask/img"+str(i)+".jpg"
    print("processing image " + input_image_path)
    # open our image, convert to rgba
    img = Image.open(input_image_path).convert('RGBA')

    # two images we'll need, glasses and deal with it text
    deal = Image.open("deals.png")


    if img.size[0] > max_width:
        scaled_height = int(max_width * img.size[1] / img.size[0])
        img.thumbnail((max_width, scaled_height))

    img_gray = np.array(img.convert('L')) # need grayscale for dlib face detection

    rects = detector(img_gray, 0)

    if len(rects) == 0:
        print("No faces found, exiting.")

    print("%i faces found in source image. processing into jpg now." % len(rects))

    faces = []

    for rect in rects:
        face = {}
        print(rect.top(), rect.right(), rect.bottom(), rect.left())
        shades_width = rect.right() - rect.left()
        shades_width += 120

        # predictor used to detect orientation in place where current face is
        shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)

        # grab the outlines of each eye from the input image
        # leftEye = shape[36:42]
        # rightEye = shape[42:48]
        mouth = shape[49:68]

        # compute the center of mass for each eye
        # leftEyeCenter = leftEye.mean(axis=0).astype("int")
        # rightEyeCenter = rightEye.mean(axis=0).astype("int")
        mouthCenter = mouth.mean(axis = 0).astype("int")

        # resize glasses to fit face width
        current_deal = deal.resize((shades_width, int(shades_width * deal.size[1] / deal.size[0])), resample=Image.LANCZOS)
        # rotate and flip to fit eye centers
        # current_deal = current_deal.rotate(angle, expand=True)
        # current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

        # add the scaled image to a list, shift the final position to the
        # left of the leftmost eye
        face['glasses_image'] = current_deal
        mouth_x = mouth[0,0] - shades_width // 4
        mouth_x -= 70
        mouth_y = mouth[0,1] - shades_width // 6
        mouth_y -= 30
        face['final_pos'] = (mouth_x, mouth_y)
        faces.append(face)

    draw_img = img.convert('RGB')
    draw_img.paste(face['glasses_image'], face['final_pos'], face['glasses_image'])
    final_image_path = "dataset/with_mask/final"+str(i)+".jpg"
    draw_img = draw_img.save(final_image_path)
