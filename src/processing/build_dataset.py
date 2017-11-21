import numpy as np
import scipy
from sklearn import svm

import filters
import parse

FOLDER = "client/dataset01/"
DEBUG = True

files = []
dataset = []
labels = []

files += parse.get_filenames(FOLDER + "forward")
files += parse.get_filenames(FOLDER + "left")
files += parse.get_filenames(FOLDER + "right")

for i, f in enumerate(files):
    print("Handling file %s" % f)
    dataset.append(f)
    labels.append(parse.labelize_dir(f))

np.save("dataset", dataset)
np.save("labels", labels)
