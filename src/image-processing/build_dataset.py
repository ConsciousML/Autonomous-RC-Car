import parse
import numpy as np
import filters
from sklearn import svm

FOLDER = "client/pictures/"
DATASET_NAME = "D2-test1/"
DEBUG = True

files = parse.get_filenames(FOLDER + DATASET_NAME)
size = filters.binarize(files[0], 200).size
dataset = np.ones((len(files), size))
labels = np.ones(len(files))

for i, f in enumerate(files):
    if DEBUG:
        print("Handling file %s" % f)
    binary = filters.binarize(f, 200)
    dataset[i] = binary.reshape(size)
    labels[i] = parse.labelize(f)

np.save("dataset", dataset)
np.save("labels", labels)
