from keras.preprocessing.image import ImageDataGenerator
from keras.backend import clear_session
from tensorflow.keras.optimizers import SGD, Adam
from pathlib import Path
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Flatten, AveragePooling2D, BatchNormalization
from keras import initializers, regularizers
from pathlib import Path
from keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau, History, LearningRateScheduler
from datetime import datetime
from time import time

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import warnings
import os

# Ignore Warnings
warnings.filterwarnings("ignore")

def main():
    # Dataset Folders
    train_neutral = (len([iq for iq in os.scandir('dataset/train/neutral')]))
    test_neutral = (len([iq for iq in os.scandir('dataset/test/neutral')]))

    train_porn = (len([iq for iq in os.scandir('dataset/train/porn')]))
    test_porn = (len([iq for iq in os.scandir('dataset/test/porn')]))

    train_sexy = (len([iq for iq in os.scandir('dataset/train/sexy')]))
    test_sexy = (len([iq for iq in os.scandir('dataset/test/sexy')]))

    # Test & Train Lists
    train_data = [train_neutral, train_porn, train_sexy]
    test_data = [test_neutral, test_porn, test_sexy]

    print(f'Total number of train data is : {train_data[0]} + {train_data[1]} + {train_data[2]} = {sum(train_data)}')
    print(f'Total number of test data is : {test_data[0]} + {test_data[1]} + {test_data[2]} = {sum(test_data)}')

    train_path =r"dataset/train"
    test_path = r"dataset/test"

    print("Example of the data Neutral and Sexy category")
    f, (ax1, ax2) = plt.subplots(1, 2)
    img=mpimg.imread(test_path+"/neutral/ffdb5729-8bac-4add-bbc1-41d1e428c842.jpg")
    ax1.imshow(img)
    img=mpimg.imread(test_path+"/sexy/ffc15b09-10a0-4753-9adf-d38eb53cf8a1.jpg")
    ax2.imshow(img)

    # As we know the input size in ImageNet was 224 so we have to resize our images accordingly
    size = 224
    epochs = 100
    steps = 500

    train_data_generation = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        channel_shift_range=20,
        horizontal_flip=True
    )
    validation_data_generation = ImageDataGenerator(
        rescale=1./255 #need float values
    )

    train_generator = train_data_generation.flow_from_directory(
        train_path,
        target_size=(size, size),
        class_mode='categorical',
        batch_size = 64
    )
    validation_generator = validation_data_generation.flow_from_directory(
        test_path,
        target_size=(size, size),
        class_mode='categorical',
        batch_size = 64
    )

    conv_m = MobileNetV2(weights='imagenet', include_top=False, input_shape=(size, size, 3))
    conv_m.trainable = False
    conv_m.summary()

    model = Sequential()
    model.add(conv_m)
    model.add(AveragePooling2D(pool_size=(7, 7)))
    model.add(Flatten())
    model.add(Dense(32, activation = 'relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))
    model.summary()

    filepath = "bestweight.h5"
    checkpoint = ModelCheckpoint("weights{epoch:05d}.h5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), patience=5, verbose=1, cooldown=0, min_lr=0.5e-6)
    callbacks = [checkpoint, lr_reduce]

    model.compile(
        loss='categorical_crossentropy',
        optimizer=SGD(lr = 0.1, momentum = 0.9),
        metrics=['accuracy']
    )

    start = datetime.now()
    history = model.fit_generator(
        train_generator,
        callbacks=callbacks,
        epochs=100,
        steps_per_epoch=10,
        validation_data=validation_generator,
        validation_steps=10,
        initial_epoch = 30
    )

    print("time taken : ", datetime.now() - start)




if __name__ == '__main__':
    main()