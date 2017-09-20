import parse
import numpy as np
import filters
from sklearn import svm

FOLDER = "client/pictures/"

files = parse.get_filenames(FOLDER)
size = filters.binarize(files[0], 200).size
dataset = np.ones((len(files), size))
labels = np.ones(len(files))
for i, f in enumerate(files):
    binary = filters.binarize(f, 200)
    dataset[i] = binary.reshape(size)
    labels[i] = parse.labelize(f)

np.save("dataset", dataset)
np.save("labels", labels)
