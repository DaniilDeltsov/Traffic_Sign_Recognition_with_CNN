from config import *
import cv2
from PIL import Image
from tqdm import tqdm
import numpy as np
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, BatchNormalization, Flatten, Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint

from sklearn.model_selection import train_test_split

num_classes = len(os.listdir("C:/Users/Daniil/Jupyter/SignsData/Train"))

# store images info and class labels to array
img_info = []
img_class = []

# loop through all folders to get images
for folder in tqdm(range(num_classes)):
    path = "C:/Users/Daniil/Jupyter/SignsData/Train/" + str(folder)
    images = os.listdir(path)

    # collect and resize every single image
    for img in images:
        try:
            # for easier manipulating PIL.Image is used
            image = cv2.imread(path + "/" + img)
            image = Image.fromarray(image, "RGB")
            image = image.resize((IMG_HEIGHT, IMG_WIDTH))
            img_info.append(np.array(image))
            img_class.append(folder)
        except:
            print("Error occured in:", img)

# convert to array
img_info = np.array(img_info)
img_class = np.array(img_class)

# shuffle all training images (classes should be shuffled the same way)
index_shuffler = np.arange(img_info.shape[0])
np.random.shuffle(index_shuffler)

img_info = img_info[index_shuffler]
img_class = img_class[index_shuffler]

# shuffle again just to be pretty sure
X_train, X_val, y_train, y_val = train_test_split(img_info, img_class, test_size=0.25, random_state=42, shuffle=True)

# normalize data to have all images from 0 to 1
X_train = X_train / 255
X_val = X_val / 255

# encode class labels
y_train = to_categorical(y_train, num_classes)
y_val = to_categorical(y_val, num_classes)

model = Sequential([
    # start block
    Conv2D(filters=16, kernel_size=(3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    Conv2D(filters=32, kernel_size=(3, 3), activation="relu"),
    MaxPool2D(pool_size=(2, 2)),
    BatchNormalization(axis=-1),

    # middle block
    Conv2D(filters=64, kernel_size=(3, 3), activation="relu"),
    Conv2D(filters=128, kernel_size=(3, 3), activation="relu"),
    MaxPool2D(pool_size=(2, 2)),
    BatchNormalization(axis=-1),

    # final block
    Flatten(),
    Dense(512, activation="relu"),
    BatchNormalization(),
    Dropout(rate=0.5),

    # output
    Dense(205, activation="softmax")
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE, decay=LEARNING_RATE * 1 / 2),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

# data augmentation online
augmentator = ImageDataGenerator(rotation_range=10,
                                 zoom_range=0.15,
                                 height_shift_range=0.1,
                                 width_shift_range=0.1,
                                 shear_range=0.15)

cp_callback = ModelCheckpoint(filepath="C:/Users/Daniil/Desktop/weights.h5", save_weights_only=True, verbose=1)

history = model.fit(augmentator.flow(X_train, y_train, batch_size=BATCH_SIZE)
                    , epochs=EPOCHS, validation_data=(X_val, y_val), callbacks=[cp_callback])

# save model
model_json = model.to_json()
with open("model.json", 'w') as f:
    f.write(model_json)
