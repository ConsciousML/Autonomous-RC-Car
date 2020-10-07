import os
import sys
import cv2
import glob
import argparse
import numpy as np
from datetime import datetime

from keras.models import Model
from keras.layers import Input
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import MaxPooling1D
from keras.optimizers import SGD
from sklearn.preprocessing import OneHotEncoder
from keras.applications.mobilenet import preprocess_input
from keras.utils import to_categorical

sys.path.append(os.getcwd())
from smartcar.learn.model import StopCNN

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--true_dir', type=str, default='data' + os.path.sep + 'true', nargs='?', 
        help='The directory containing positive image i.e images of stop sign.')
    parser.add_argument('--false_dir', type=str, default='data' + os.path.sep + 'false', nargs='?', 
        help='The directory containing positive image i.e images of stop sign.')
    parser.add_argument('--epochs', type=int, default=30, nargs='?', 
        help='The number of epochs.')
    parser.add_argument('--out_dir', type=str, default='tmp', nargs='?', 
        help='The output directory to store best model and training curves.')
    args = parser.parse_args()

    now = datetime.now()
    model_fname = now.strftime("%d_%m_%Y_%H_%M_%S") + '.h5'

    positives = []
    for filen in glob.glob(os.path.join(args.true_dir, '*')):
        imgrgb = cv2.imread(filen, 1)
        imgrgb = cv2.resize(imgrgb, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
        positives.append(imgrgb)
    positives = np.array(positives)

    negatives = []
    for filen in glob.glob(os.path.join(args.false_dir, '*')):
        imgrgb = cv2.imread(filen, 1)
        imgrgb = cv2.resize(imgrgb, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
        negatives.append(imgrgb)
    negatives = np.array(negatives)

    labels = np.ones(len(positives))
    labels = np.concatenate((labels, np.zeros(negatives.shape[0])))

    data = np.concatenate((positives, negatives))

    idx = np.random.permutation(data.shape[0])
    data, labels = data[idx], labels[idx]

    model = StopCNN()

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    data = preprocess_input(data.astype(float))
    labels = to_categorical(labels)

    model.fit(data, labels, epochs=args.epochs)

    model_save_path = os.path.join(args.out_dir, model_fname)
    model.save(model_save_path)

    print('Best model saved in: ' + model_save_path)
