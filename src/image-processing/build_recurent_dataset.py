import numpy as np
import scipy
from sklearn import svm
from PIL import Image
import cv2

import filters
import parse

FOLDER = "../server/"
DATASET_NAME = "pictures/"
SIZE = 80*60
DEBUG = False

files = parse.get_filenames(FOLDER + DATASET_NAME)
<<<<<<< HEAD
dataset = np.ones((len(files), SIZE * 2))
=======
dataset = np.ones((len(files), SIZE * 2 + 1))
>>>>>>> 1fcd469ae1163836001dfceee4e516e31297f425
labels = np.ones(len(files))

class Counter:
    i = 0

# Pipeline
def process_image(filename):
<<<<<<< HEAD
    img = filters.binarize(filename, 160)
    img = scipy.misc.imresize(img, (80, 60), interp="nearest")
    if DEBUG:
        scipy.misc.imsave(FOLDER + "tmp/" + str(Counter.i).zfill(3) + ".jpg", img)
        Counter.i += 1
    img = img.reshape(SIZE)
=======
    img = Image.open(filename)
    img = np.array(img)
    img = scipy.misc.imresize(img, (80, 60))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = filters.bin_array(img)
    if DEBUG:
        scipy.misc.imsave(FOLDER + "tmp/" + str(Counter.i).zfill(3) + ".jpg", img)
        Counter.i += 1
    img = img.reshape(1, -1)
>>>>>>> 1fcd469ae1163836001dfceee4e516e31297f425
    return img


files = sorted(files)
print(files)
img_1 = None
img_0 = None
<<<<<<< HEAD
=======
label_1 = None
>>>>>>> 1fcd469ae1163836001dfceee4e516e31297f425
for i, f in enumerate(files):
    print "Handling file", f

    img_0 = process_image(f)
    if img_1 is None:
<<<<<<< HEAD
        dataset[i] = np.append(img_0, img_0)
    else:
        dataset[i] = np.append(img_0, img_1)
    img_1 = img_0
    labels[i] = parse.labelize(f)
=======
        imgs = np.append(img_0, img_0)
        dataset[i] = np.append(imgs, parse.labelize(f))
    else:
        imgs = np.append(img_0, img_1)
        dataset[i] = np.append(imgs, label_1)
    img_1 = img_0
    label_1 = parse.labelize(f)
    labels[i] = label_1
>>>>>>> 1fcd469ae1163836001dfceee4e516e31297f425

np.save("dataset_recurent", dataset)
np.save("labels_recurent", labels)
