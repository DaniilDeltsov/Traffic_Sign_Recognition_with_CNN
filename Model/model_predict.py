import numpy as np
from PIL import Image
import cv2
from tensorflow.keras.models import model_from_json
from config import *

with open("model.json", 'r') as f:
    loaded_model = model_from_json(f.read())
loaded_model.load_weights("weights.h5")

def make_prediction(image):
    data = []
    img = cv2.imread(image)
    img_from_array = Image.fromarray(img)
    resized_img = img_from_array.resize((IMG_HEIGHT, IMG_WIDTH))
    data.append(np.array(resized_img))

    X_test = np.array(data)
    X_test = X_test / 255

    pred = np.argmax(loaded_model.predict(X_test), axis=-1)
    if int(pred) in classes.keys():
        return f"Я думаю, что это знак: {classes[int(pred)]}."
    else:
        return "К сожалению, я пока что еще не знаю такой знак... :("
