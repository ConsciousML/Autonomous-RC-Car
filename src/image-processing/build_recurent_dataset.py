import numpy as np
import scipy
from sklearn import svm

import filters
import parse

FOLDER = "server/"
DATASET_NAME = "pictures/"
SIZE = 80*60
DEBUG = False

files = parse.get_filenames(FOLDER + DATASET_NAME)
dataset = np.ones((len(files), SIZE * 2))
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


files = sorted(files)
print(files)
img_1 = None
img_0 = None
for i, f in enumerate(files):
    print "Handling file", f

    img_0 = process_image(f)
    if img_1 is None:
        dataset[i] = np.append(img_0, img_0)
    else:
        dataset[i] = np.append(img_0, img_1)
    img_1 = img_0
    labels[i] = parse.labelize(f)

np.save("dataset_recurent", dataset)
np.save("labels_recurent", labels)
