import parse
import numpy as np
import filters

files = parse.get_filenames("client/pictures/", "test7-parfait")
binary = filters.binarize(files[0], 200)
dataset = np.ones((len(files), binary.size))
labels = np.ones(len(files))
for i, f in enumerate(files):
    binary = filters.binarize(f, 200)
    dataset[i] = binary.reshape(binary.size)
    labels[i] = parse.labelize(f)
