import numpy as np
import scipy
from sklearn import svm

import filters
import parse

FOLDER = "client/"
DATASET_NAME = "pictures/"
SIZE = 80*60
DEBUG = False

files = parse.get_filenames(FOLDER + DATASET_NAME)
dataset = np.ones((len(files), SIZE))
labels = np.ones(len(files))

class Counter:
    i = 0

# Pipeline
def process_image(filename):
    img = filters.binarize(filename, 160)
    img = scipy.misc.imresize(img, (80, 60), interp="nearest")
    if DEBUG:
        scipy.misc.imsave(FOLDER + "tmp/" + str(Counter.i).zfill(3) + ".jpg", img)
        Counter.i += 1
    img = img.reshape(SIZE)
    return img


for i, f in enumerate(files):
    if DEBUG:
        print("Handling file %s" % f)
    dataset[i] = process_image(f)
    labels[i] = parse.labelize(f)

np.save("dataset", dataset)
np.save("labels", labels)
