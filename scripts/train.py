import sys
import cv2
import numpy as np

from keras.optimizers import Adam
from keras.utils import Sequence
from keras.callbacks import ModelCheckpoint
from keras.layers import Input, Dense
from keras.models import Model
from keras.layers import Convolution2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Dense, GlobalAveragePooling2D
from sklearn.model_selection import train_test_split

sys.path.append('..')
from smartcar.utils.path import get_data_paths
"""

This scripts trains the model that controls the speed and angle
of the autonomous remote-controlled car.

"""

if __name__ == "__main__":
    data_dir = "C:\Projects\SmartCar\data"
    batch_size = 16

    image_fnames, label_fnames = get_data_paths(data_dir)
    
