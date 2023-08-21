import cv2
import numpy as np
import time
import tensorflow as tf
import os
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

# Define the classes for bird breeds
bird_breeds = [
    'Blackbird',
    'Bluetit',
    'Carrion_Crow',
    'Chaffinch',
    'Coal_Tit',
    'Collared_Dove',
    'Dunnock',
    'Feral_Pigeon',
    'Goldfinch',
    'Great_Tit',
    'Greenfinch',
    'House_Sparrow',
    'Jackdaw',
    'Long_Tailed_Tit',
    'Magpie',
    'Robin',
    'Song_Thrush',
    'Starling',
    'Wood_Pigeon',
    'Wren'
]

MODEL_PATH = 'model.h5'

# Load the pre-trained model
model = load_model(MODEL_PATH)

def preprocess_frame(frame):
    image_width, image_height = 150, 150
    resized_frame = cv2.resize(frame, (image_width, image_height))
    normalized_frame = resized_frame / 255.0
    return np.expand_dims(normalized_frame, axis=0)

def classify_bird(image):
    preprocessed_image = preprocess_frame(image)
    predictions = model.predict(preprocessed_image)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_label = bird_breeds[predicted_class_index]
    return predicted_class_label