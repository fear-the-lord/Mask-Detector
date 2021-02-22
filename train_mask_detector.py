# Import the necessary dependencies
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os

# Initialize the initial learning rate, number of epochs to train for, and batch size
# Lower Learning rate for better learning
INIT_LR = 1e-4
EPOCHS = 20
BS = 32
# Fix the image size and the image channels
IMAGE_SIZE = 224
CHANNEL = 3

# Get the path to the dataset
DIRECTORY = r"C:\Users\admin\Desktop\Mask Detector\dataset"
CATEGORIES = ["with_mask", "without_mask"]

# Grab the list of images in our dataset directory, then initialize the list of data (i.e., images) and class images
print("[INFO] Loading Images...")

data = []
labels = []

# Loop over all the categories
for category in CATEGORIES:
	# Enter into the dataset of a particular category
    path = os.path.join(DIRECTORY, category)
    # Loop over all the images of that category
    for img in os.listdir(path):
    	# Get hold of a particular image
    	img_path = os.path.join(path, img)
    	# Load the image
    	image = load_img(img_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    	# Convert the image to an array
    	image = img_to_array(image)
    	# Preprocess the image
    	image = preprocess_input(image)

    	data.append(image)
    	labels.append(category)

# Perform one-hot encoding on the labels, so that the labels are converted to integers
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

# Convert the image and labels both into numpy array, because we need numpy arrays in case of training
data = np.array(data, dtype = "float32")
labels = np.array(labels)

# Split the dataset into training and test data
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size = 0.20, stratify = labels, random_state = 20)

# Construct the training image generator for data augmentation
aug = ImageDataGenerator(
	rotation_range = 20,
	zoom_range = 0.15,
	width_shift_range = 0.2,
	height_shift_range = 0.2,
	channel_shift_range = 0.2,
	shear_range = 0.15,
	horizontal_flip = True,
	zca_whitening = True,
	zca_epsilon = 1e-06,
	featurewise_center = True,
    featurewise_std_normalization = True,
	fill_mode = "nearest")

# Load the MobileNetV2 network, ensuring the head FC layer sets are left off
baseModel = MobileNetV2(weights = "imagenet", include_top = False, input_tensor = Input(shape = (IMAGE_SIZE, IMAGE_SIZE, CHANNEL)))

# Construct the head of the model that will be placed on top of the the base model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size = (7, 7))(headModel)
headModel = Flatten(name = "flatten")(headModel)
headModel = Dense(128, activation = "relu")(headModel)
# Dropuout to prevent overfitting
headModel = Dropout(0.5)(headModel)
# Since there are only 2 classes, so 2 outputs are required
headModel = Dense(2, activation = "softmax")(headModel)

# Place the head FC model on top of the base model (this will become the actual model we will train)
model = Model(inputs = baseModel.input, outputs = headModel)

# Loop over all layers in the base model and freeze them so they will
# *not* be updated during the first training process
for layer in baseModel.layers:
	layer.trainable = False

# Compile the model
print("[INFO] Compiling The Model...")
opt = Adam(lr = INIT_LR, decay = INIT_LR / EPOCHS)
model.compile(loss = "binary_crossentropy", optimizer = opt, metrics = ["accuracy"])

# Train the model
print("[INFO] Training The Model...")
H = model.fit(
	aug.flow(trainX, trainY, batch_size = BS),
	steps_per_epoch = len(trainX) // BS,
	validation_data = (testX, testY),
	validation_steps = len(testX) // BS,
	epochs = EPOCHS)

# Make predictions on the testing set
print("[INFO] Evaluating network...")
predIdxs = model.predict(testX, batch_size = BS)

# For each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis = 1)

# Show a nicely formatted classification report
print(classification_report(testY.argmax(axis = 1), predIdxs, target_names = lb.classes_))

# Serialize the model to disk
print("[INFO] Saving Mask Detector Model...")
model.save("models/mask_detector.model", save_format = "h5")
print("[INFO] Training Successful...")

# Plot the training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label = "train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label = "val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label = "train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label = "val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Loss/Accuracy")
plt.legend(loc = "lower left")
plt.savefig("images/plot.png")