from PIL import Image
from scipy.misc import imsave
import numpy

def bin_array(numpy_array, threshold=200):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

def binarize(filename, threshold):
    """Binarize an image """
    file = Image.open(filename)
    file = file.convert('L') # 'L' is monochrome, '1' is black and white
    file = numpy.array(file)
    file = bin_array(file, threshold)
    imsave('lol.jpg', file)

binarize("client/pictures/test7-parfait/164forward.jpg", 210)

