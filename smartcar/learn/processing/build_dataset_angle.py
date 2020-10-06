import numpy as np
from scipy.misc import imread, imresize
from sklearn import svm
from random import shuffle
from sklearn.cross_validation import train_test_split

from src.learning.processing import filters
from src.learning.processing import parse

NPY_DATA_NAME_TRAIN = "train_angle_dataset"
NPY_DATA_NAME_TEST = "test_angle_dataset"
NPY_LABELS_NAME_TRAIN = "train_angle_labels"
NPY_LABELS_NAME_TEST = "test_angle_labels"

def min(a, b) : return a if a < b else b

def dump_npy():
    FOLDER = "datasets/pictures/"
    DEBUG = True

    files = []
    dataset = []
    labels = []

    files_l1 = parse.get_filenames(FOLDER + "left_dataset")
    #files += files_l1
    #files_l1 = parse.get_filenames(FOLDER + "right_dataset")
    files += files_l1
    '''
    min_len = len(files_l1)
    files_l2 = parse.get_filenames(FOLDER + "right_dataset")
    min_len = min(min_len, len(files_l2))
    print(min_len)

    shuffle(files_l1)
    shuffle(files_l2)

    files += files_l1[:min_len]
    files += files_l2[:min_len]

    print(len(files))
    '''


    for i, f in enumerate(files):
        dataset.append(f)
        labels.append(parse.labelize_angle(f))

    dataset = np.array(dataset)
    labels = np.array(labels)

    #X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.33)
    #np.save(NPY_DATA_NAME_TRAIN, X_train)
    #np.save(NPY_DATA_NAME_TEST, X_test)
    #np.save(NPY_LABELS_NAME_TRAIN, y_train)
    #np.save(NPY_LABELS_NAME_TEST, y_test)
    np.save("a_dataset", dataset)
    np.save("a_labels", labels)

def readNshape(img):
    file = imread(img)
    file = imresize(file, (224, 224))
    return file

def gen_data(f_dataset, f_labels, batch_size, test_rate=0.3):
    '''
    f_dataset : nom du fichier .npy où sont les noms des fichiers
    f_labels : nom du fichier .npy où se trouvent les labels
    batch_size : le nombre de fichiers à envoyer par batch
    '''
    dump_npy()
    dataset = np.load(f_dataset)
    labels = np.load(f_labels)
    j = 0
    grappe_data = []
    grappe_labels = []


    # Validation
    idx = int(len(dataset) * test_rate)
    print("Yielding %d data as validation" % idx)
    valid_data = []
    for i in range(idx):
        valid_data.append(readNshape(dataset[i]))
        
    yield np.array(valid_data[:idx]), np.array(labels[:idx])

    dataset = dataset[idx:]
    labels = labels[idx:]

    max_size = len(dataset)
    print("Will yield a total of %d data (validation not included)" % max_size)

    while True:
        for i in range(max_size):

            if j == batch_size:# or i == max_size:
                yield np.array(grappe_data), np.array(grappe_labels)

                grappe_data = []
                grappe_labels = []
                j = 0

            grappe_data.append(readNshape(dataset[i]))
            grappe_labels.append(labels[i])
            j += 1
