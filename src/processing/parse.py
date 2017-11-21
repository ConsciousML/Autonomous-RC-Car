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
    if not filenames:
        print("Not any file found.")
        sys.exit(1)
    return filenames


class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)

"""
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
"""
def labelize(filename):
    splited_dir = filename.split("/")
    filename = splited_dir[len(splited_dir) - 1]
    splited_name = filename.split("_")
    label = splited_name[len(splited_name) - 1][:-4]
    return label
