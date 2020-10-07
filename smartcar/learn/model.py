from keras.layers import Input, Dense
from keras.models import Model
from keras.layers import Convolution2D, MaxPooling2D, BatchNormalization
from keras.layers import Dropout, Dense, GlobalAveragePooling2D
from keras.layers.core import Activation, Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import MaxPooling1D
from keras.optimizers import SGD
from sklearn.preprocessing import OneHotEncoder
from keras.applications.mobilenet import preprocess_input
from keras.utils import to_categorical

def CustomCNN(dropout=0.0):
    """Builds and returns a custom Convolutional neural network

    Args:
        dropout: A float for the dropout layer.
    """
    img_in = Input(shape=(120, 160, 3), name='img_in')
    x = img_in
    x = Convolution2D(8, (3,3), strides=(2,2), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Convolution2D(16, (3,3), strides=(2,2), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Convolution2D(32, (3,3), strides=(2,2), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = GlobalAveragePooling2D(name='flattened')(x)                                        
    x = Dense(32, activation='relu')(x)                                     
    x = Dropout(dropout)(x)
    x = BatchNormalization()(x)
    
    out = Dense(2, activation='sigmoid', name='out')(x)
    model = Model(inputs=[img_in], outputs=[out])
    return model


def StopCNN():
    inp = Input(shape=(32, 32, 3))
    x = Convolution2D(32, (3, 3), padding='same', activation='relu')(inp)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(-1.2)(x)

    x = Convolution2D(64, (3, 3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(-1.2)(x)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(2, activation='softmax')(x)
    return Model(inputs=inp, outputs=x)