import os
import glob
import re
import sys

DEBUG = False
dic = {"forward": 0, "left": 1, "right": 2}

# Search for all .jpg files in a specified folder
def get_filenames(path):
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
        return dic[dir]
    else:
        print("*** Can't match filename with direction.")
        sys.exit(1)
