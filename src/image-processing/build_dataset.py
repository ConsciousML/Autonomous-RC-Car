import parse
import numpy as np
import filters

FOLDER = "client/pictures/"
DATASET_NAME = "test7-parfait/"

files = parse.get_filenames(FOLDER + DATASET_NAME)
size = filters.binarize(files[0], 200).size
dataset = np.ones((len(files), size))
labels = np.ones(len(files))
for i, f in enumerate(files):
    binary = filters.binarize(f, 200)
    dataset[i] = binary.reshape(size)
    labels[i] = parse.labelize(f)
