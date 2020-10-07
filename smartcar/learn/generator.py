import cv2
import numpy as np
from keras.utils import Sequence
from keras.callbacks import ModelCheckpoint
from keras.layers import Input, Dense
from keras.models import Model
from keras.layers import Convolution2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Dense, GlobalAveragePooling2D
from sklearn.model_selection import train_test_split

from smartcar.utils.read import read_json_label
from smartcar.learn.brightness import randomize_brightness

class CustomGenerator(Sequence):
    """Class that yields the batch of data to the model

    Inherits from Sequence class of Keras. Every image in the batch
    is verticaly flipped and its brightness is altered for more
    robustness.

    Attributes:
        image_fnames: A list containing the paths of the images.
        label_fnames: A list containing the paths of the labels
        batch_size: A positive integer for the batch size.
        image_shape: A triple containing the (width, height, channels) of
            the images.
        shuffle: A boolean for shuffling the data.

    """

    def __init__(self, image_fnames, label_fnames, batch_size, image_shape, shuffle=True):
        """Initialize the generator class"""
        self.image_fnames = np.array(image_fnames)
        self.label_fnames = np.array(label_fnames)
        self.batch_size = batch_size
        self.image_shape = image_shape
    
        if shuffle:
            indices = np.array([i for i in range(len(image_fnames))])
            indices = np.random.permutation(indices)
            self.image_fnames = self.image_fnames[indices]
            self.label_fnames = self.label_fnames[indices]
    
    def load_image(self, path, flip=False):
        """Loads an image from path, flips and apply random brightness"""
        image = cv2.imread(path)
        image = cv2.resize(image, (self.image_shape[1], self.image_shape[0]), interpolation=cv2.INTER_NEAREST)
        if flip:
            image = cv2.flip(image, 1)
        image = randomize_brightness(image)
        return image
    
    def __len__(self):
        """Number of batches to yield"""
        return np.ceil(len(self.image_fnames) / float(self.batch_size)).astype(np.int)
                       
    def __getitem__(self, idx):
        """Yields the nth batch"""
        x_fnames = self.image_fnames[idx * self.batch_size:(idx+1) * self.batch_size]
        y_fnames = self.label_fnames[idx * self.batch_size:(idx+1) * self.batch_size]
        
        size = len(x_fnames)
        batch_x = np.zeros((size, self.image_shape[0], self.image_shape[1], 3))
        batch_y = np.zeros((size, 2))
        
        for i in range(size):
            flip = 0.5 >= np.random.rand(1)
            image = self.load_image(x_fnames[i], flip)
            batch_x[i] = image / 255.
            
            angle, speed = read_json_label(y_fnames[i])
            if flip:
                angle = 1 - angle
            batch_y[i][0] = angle
            batch_y[i][1] = speed
        return batch_x, batch_y