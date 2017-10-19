import numpy as np
import scipy
from sklearn import svm
from PIL import Image
import cv2

import filters
import parse

FOLDER = "client/"
DATASET_NAME = "pictures/"
SIZE = 80*60
DEBUG = False

files = parse.get_filenames(FOLDER + DATASET_NAME)
dataset = np.ones((len(files), SIZE * 2 + 1))
labels = np.ones(len(files))

class Counter:
    i = 0

# Pipeline
def process_image(filename):
    img = Image.open(filename)
    img = np.array(img)
    img = scipy.misc.imresize(img, (80, 60))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = filters.bin_array(img)
    if DEBUG:
        scipy.misc.imsave(FOLDER + "tmp/" + str(Counter.i).zfill(3) + ".jpg", img)
        Counter.i += 1
    img = img.reshape(1, -1)
    return img


files = sorted(files)
print(files)
img_1 = None
img_0 = None
label_1 = None
for i, f in enumerate(files):
    print "Handling file", f

    img_0 = process_image(f)
    if img_1 is None:
        imgs = np.append(img_0, img_0)
        dataset[i] = np.append(imgs, parse.labelize(f))
    else:
        imgs = np.append(img_0, img_1)
        dataset[i] = np.append(imgs, label_1)
    img_1 = img_0
    label_1 = parse.labelize(f)
    labels[i] = label_1

np.save("dataset_recurent", dataset)
np.save("labels_recurent", labels)
