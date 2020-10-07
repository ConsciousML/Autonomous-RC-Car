import os
import sys
from sklearn.model_selection import train_test_split

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
    lr = 1e-4
    batch_size = 16
    model_save_path = 'test.h5' 
    epochs = 20

    image_fnames, label_fnames = get_data_paths(data_dir)
    X_train, X_test, y_train, y_test = train_test_split(image_fnames, label_fnames, train_size=0.80, random_state=42)

    datagen_train = CustomGenerator(X_train, y_train, batch_size=16, image_shape=(120, 160, 3), shuffle=True)
    datagen_test = CustomGenerator(X_test, y_test, batch_size=16, image_shape=(120, 160, 3), shuffle=True)

    model = CustomCNN()

    opt = Adam(learning_rate=lr)
    model.compile(optimizer=opt,
              loss={'out' : 'mean_squared_error'})    

    model_path = os.path.abspath(model_save_path)
    checkpointer = ModelCheckpoint(model_path, save_best_only=True, monitor='val_loss', mode='min')
    hist = model.fit_generator(generator=datagen_train,
                           validation_data=datagen_test,
                           epochs=epochs,
                           shuffle=True,
                           callbacks=[checkpointer])
    print('Best model saved to: ' + model_save_path)
     
