import sys
import cv2
import numpy as np

from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.utils import Sequence
from keras.callbacks import ModelCheckpoint
from keras.models import Model
from keras.layers import Input, Dense
from keras.layers import Convolution2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Dense, GlobalAveragePooling2D

sys.path.append('..')
from smartcar.utils.path import get_data_paths
from smartcar.learn.model import CustomCNN
from smartcar.learn.generator import CustomGenerator
"""

This scripts trains the model that controls the speed and angle
of the autonomous remote-controlled car.

"""

if __name__ == "__main__":
    data_dir = "C:\Projects\SmartCar\data"
    batch_size = 16

    image_fnames, label_fnames = get_data_paths(data_dir)
    X_train, X_test, y_train, y_test = train_test_split(image_fnames, label_fnames, train_size=0.80, random_state=42)

    datagen_train = CustomGenerator(X_train, y_train, batch_size=16, image_shape=(120, 160, 3), shuffle=True)
    datagen_test = CustomGenerator(X_test, y_test, batch_size=16, image_shape=(120, 160, 3), shuffle=True)

    model = CustomCNN()
     
