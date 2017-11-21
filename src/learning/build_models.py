from keras.applications.mobilenet import MobileNet
from keras.layers import Recurrent, Dense
from keras.models import Model
import numpy as np

def RecurrentMobileNet():
    model = MobileNet()
    # Remove last layers
    last_layer = model.layers[-6]
    out = last_layer.output
    out = Recurrent()(out)
    out = Dense(1, activation="sigmoid")(out)

    my_model = Model(model.layers[0].input, out)

    idx = my_model.layers.index(last_layer)

    for i in range(idx):
        my_model.layers[i].trainable = False
    for i in range(idx, len(my_model.layers)):
        my_model.layers[i].trainable = True

    my_model.compile(loss='mse',
            optimizer='adam',
            metrics=['mse'])
    return my_model

