import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import os
import random
import shutil

# Define the paths
base_dir = "/Users/ioanevans/Documents/BirdsData"
archive_dir = os.path.join(base_dir, "archive")
train_dir = os.path.join(base_dir, "train")
validation_dir = os.path.join(base_dir, "validation")

# Create the train and validation folders
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# List all bird categories
bird_categories = ["Blackbird", "Bluetit", "Carrion_Crow", "Chaffinch", "Coal_Tit", "Collared_Dove",
                   "Dunnock", "Feral_Pigeon", "Goldfinch", "Great_Tit", "Greenfinch", "House_Sparrow",
                   "Jackdaw", "Long_Tailed_Tit", "Magpie", "Robin", "Song_Thrush", "Starling", "Wood_Pigeon", "Wren"]

# Move 80% of images to train folders
for bird_name in bird_categories:
    bird_archive_dir_with_bg = os.path.join(archive_dir, "withBackground", bird_name)
    bird_train_dir = os.path.join(train_dir, bird_name)
    os.makedirs(bird_train_dir, exist_ok=True)
    
    bird_images = os.listdir(bird_archive_dir_with_bg)
    random.shuffle(bird_images)
    num_train_images = int(len(bird_images) * 0.8)
    
    for img in bird_images[:num_train_images]:
        src = os.path.join(bird_archive_dir_with_bg, img)
        dst = os.path.join(bird_train_dir, img)
        shutil.copyfile(src, dst)

# Move the remaining 20% of images to validation folders
for bird_name in bird_categories:
    bird_archive_dir_with_bg = os.path.join(archive_dir, "withBackground", bird_name)
    bird_validation_dir = os.path.join(validation_dir, bird_name)
    os.makedirs(bird_validation_dir, exist_ok=True)
    
    bird_images = os.listdir(bird_archive_dir_with_bg)
    random.shuffle(bird_images)
    num_train_images = int(len(bird_images) * 0.8)
    
    for img in bird_images[num_train_images:]:
        src = os.path.join(bird_archive_dir_with_bg, img)
        dst = os.path.join(bird_validation_dir, img)
        shutil.copyfile(src, dst)

# Define data augmentation parameters
image_height = 150
image_width = 150
batch_size = 32

# Data augmentation for training data
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

# Data augmentation for validation data (only rescaling)
val_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Load training data from the train directory
train_data_dir = "/Users/ioanevans/Documents/BirdsData/train"
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='categorical',    # For multi-class classification
)

# Load validation data from the validation directory
validation_data_dir = "/Users/ioanevans/Documents/BirdsData/validation"
val_generator = val_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(image_height, image_width),
    batch_size=batch_size,
    class_mode='categorical', 
)
# Step 4: Define the Neural Network Model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(20, activation='softmax'))

# Step 5: Compile the Model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Step 6: Training 
# Number of training steps per epoch (total number of training samples / batch size)
steps_per_epoch = len(train_generator)

# Number of validation steps (total number of validation samples / batch size)
validation_steps = len(val_generator)

# Train the model using the train_generator for training data and val_generator for validation data
history = model.fit(train_generator, epochs=10, steps_per_epoch=steps_per_epoch,
                    validation_data=val_generator, validation_steps=validation_steps)

#Step 7 - Validation
validation_loss, validation_accuracy = model.evaluate(val_generator)
print("Accuracy:", validation_accuracy)
