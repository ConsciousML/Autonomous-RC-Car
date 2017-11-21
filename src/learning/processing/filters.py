from PIL import Image
from scipy.misc import imsave
import numpy as np

def bin_array(numpy_array, threshold=160):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

def bin_image(img, threshold=170):
    file = img.convert('L') # 'L' is monochrome, '1' is black and white
    file = np.array(file)
    file = bin_array(file, threshold)
    return file

def binarize(filename, threshold=170):
    """Binarize an image """
    file = Image.open(filename)
    return bin_image(file, threshold)
