import numpy as np
from scipy.misc import imread, imresize
from sklearn import svm

from processing import filters
from processing import parse

NPY_DATA_NAME = "dataset"
NPY_LABELS_NAME = "labels"

def dump_npy():
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

    np.save(NPY_DATA_NAME, dataset)
    np.save(NPY_LABELS_NAME, labels)

def readNshape(img):
    file = imread(img)
    file = imresize(file, (224, 224))
    return file

def gen_data(f_dataset, f_labels, batch_size):
    '''
    f_dataset : nom du fichier .npy où sont les noms des fichiers
    f_labels : nom du fichier .npy où se trouvent les labels
    batch_size : le nombre de fichiers à envoyer par batch
    '''
    dataset = np.load(f_dataset)
    labels = np.load(f_labels)
    j = 0
    grappe_data = []
    grappe_labels = []

    max_size = len(dataset)
    for i in range(max_size):

        if j == batch_size or i == max_size:
            yield np.array(grappe_data), np.array(grappe_labels)

            grappe_data = []
            grappe_labels = []
            j = 0

        grappe_data.append(readNshape(dataset[i]))
        grappe_labels.append(labels[i])
        j += 1
