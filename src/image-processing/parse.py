import os
import glob

FOLDER = "client/pictures/"
DATASET_NAME = "test7-parfait"
DEBUG = True

# Search for all .jpg files in a specified folder
def get_filenames(FOLDER, DATASET_NAME):
    path = FOLDER + DATASET_NAME + "/"
    if DEBUG:
        print("Opening folder %s" % path)
    filenames = []
    for infile in glob.glob(os.path.join(path, '*.jpg')):
        if DEBUG:
            print("File is: %s" % infile)
        filenames.append(infile)
    return filenames


