from keras.layers import Input, Dense
from keras.models import Model
from keras.layers import Convolution2D, MaxPooling2D, BatchNormalization
from keras.layers import Dropout, Dense, GlobalAveragePooling2D

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