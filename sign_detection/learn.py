import cv2
import glob
import numpy as np

from keras.models import Model
from keras.layers import Input
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD

from sklearn.preprocessing import OneHotEncoder
from keras.applications.mobilenet import preprocess_input
from keras.utils import to_categorical

def cnn_model():
    inp = Input(shape=(32, 32, 3))
    x = Conv2D(32, (3, 3), padding='same', activation='relu')(inp)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(0.2)(x)

    x = Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(0.2)(x)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(2, activation='softmax')(x)
    return Model(inputs=inp, outputs=x)

positives = []
for filen in glob.glob("true/*"):
    imgrgb = cv2.imread(filen, 1)
    imgrgb = cv2.resize(imgrgb, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
    positives.append(imgrgb)
positives = np.array(positives)
print "Positive:", positives.shape

negatives = []
for filen in glob.glob("false/*"):
    imgrgb = cv2.imread(filen, 1)
    imgrgb = cv2.resize(imgrgb, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
    negatives.append(imgrgb)
negatives = np.array(negatives)
print "Negative:", negatives.shape

labels = np.ones(len(positives))
labels = np.concatenate((labels, np.zeros(negatives.shape[0])))

data = np.concatenate((positives, negatives))

idx = np.random.permutation(data.shape[0])
data, labels = data[idx], labels[idx]

model = cnn_model()

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

data = preprocess_input(data.astype(float))
labels = to_categorical(labels)

model.fit(data, labels, epochs=30)

model.save('../models/sign_classification.h5')
