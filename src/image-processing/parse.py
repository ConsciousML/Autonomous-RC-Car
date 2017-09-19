import os
import glob
import re
import sys

FOLDER = "client/pictures/"
DATASET_NAME = "test7-parfait/"
DEBUG = True

file = FOLDER + DATASET_NAME + "168forward.jpg"

# Search for all .jpg files in a specified folder
def get_filenames(FOLDER, DATASET_NAME):
    path = FOLDER + DATASET_NAME
    if DEBUG:
        print("Opening folder %s" % path)
    filenames = []
    for infile in glob.glob(os.path.join(path, '*.jpg')):
        if DEBUG:
            print("File is: %s" % infile)
        filenames.append(infile)
    return filenames


class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)


def labelize(filename):
    m = REMatcher(filename)
    if m.match(r"(.*/)*(\w+).jpg$"):
        dir = m.group(2)
        dir = re.sub("\d+", "", dir)
        if DEBUG:
            print("dir is %s" % dir)
        return dir
    else:
        print("*** Can't match filename with direction.")
        sys.exit(1)

labelize(file)
