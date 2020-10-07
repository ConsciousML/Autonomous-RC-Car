import os
import sys
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

sys.path.append(os.getcwd())
from smartcar.utils.path import get_data_paths
from smartcar.learn.model import PilotCNN
from smartcar.learn.generator import CustomGenerator

"""

This scripts trains the model that controls the speed and angle
of the autonomous remote-controlled car.

"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data' + os.path.sep + 'tracks', nargs='?', 
        help='The directory containing the training data.')
    parser.add_argument('--out_dir', type=str, default='tmp', nargs='?', 
        help='The output directory to store best model and training curves.')
    parser.add_argument('--lr', type=float, default=1e-4, nargs='?', 
        help='The learning rate.')
    parser.add_argument('--batch_size', type=int, default=16, nargs='?', 
        help='The batch size.')
    parser.add_argument('--epochs', type=int, default=20, nargs='?', 
        help='The number of epochs.')
    args = parser.parse_args()

    data_dir = args.data_dir
    output_dir = args.out_dir
    lr = args.lr
    batch_size = args.batch_size
    epochs = args.epochs

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    image_fnames, label_fnames = get_data_paths(data_dir)
    X_train, X_test, y_train, y_test = train_test_split(image_fnames, label_fnames, train_size=0.80, random_state=42)

    datagen_train = CustomGenerator(X_train, y_train, batch_size=16, image_shape=(120, 160, 3), shuffle=True)
    datagen_test = CustomGenerator(X_test, y_test, batch_size=16, image_shape=(120, 160, 3), shuffle=True)

    model = PilotCNN()

    opt = Adam(learning_rate=lr)
    model.compile(optimizer=opt,
              loss={'out' : 'mean_squared_error'})    

    model_save_path = os.path.join(output_dir, dt_string + '.h5')
    checkpointer = ModelCheckpoint(model_save_path, save_best_only=True, monitor='val_loss', mode='min')
    hist = model.fit_generator(generator=datagen_train,
                           validation_data=datagen_test,
                           epochs=epochs,
                           shuffle=True,
                           callbacks=[checkpointer])
    print('Best model saved to: ' + model_save_path)

    loss_fig_path = os.path.join(output_dir, dt_string + '.jpg')
    plt.plot(hist.history["loss"][1:])
    plt.plot(hist.history["val_loss"][1:])
    ax = plt.gca()
    ax.set_ylim([0.06, 0.11])
    plt.savefig(loss_fig_path)

    print('Save loss figure to: ' + loss_fig_path)
     
