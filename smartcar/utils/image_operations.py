import numpy as np

from bresenham import bresenham
from PIL import Image

from random import choice


def _fill_shape(mask):
    """
    Auxiliary function of generate_shape.
    Fill the shape mask

    Arguments:
        mask: mask to fill

    Returns:
        Filled mask
    """

    row, col, _ = mask.shape
    queue = []
    queue.append((0, 0))
    mask[(0, 0)] = 0
    for j in queue:
        for i in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (j[0]+i[0] < row and j[0]+i[0] > -1
                and j[1]+i[1] > -1
                and j[1]+i[1] < col
                    and mask[j[0]+i[0], j[1]+i[1]][0] == 1):

                mask[(j[0]+i[0], j[1]+i[1])] = 0
                queue.append((j[0]+i[0], j[1]+i[1]))

    return mask


def generate_shape(shape):
    """
    Generates a polygon mask

    Arguments:
        shape: base image shape

    Returns:
        Polygon mask
    """

    row, col, _ = shape
    nb_summits = np.random.randint(5, 7)
    summits = []
    for _ in range(nb_summits):
        summits.append((np.random.randint(1, row - 1),
                        np.random.randint(1, col - 1)))
    summits.append(summits[0])
    res = np.ones(shape)
    for s in range(nb_summits):
        for p in bresenham(summits[s][0], summits[s][1], summits[s+1][0], summits[s+1][1]):
            res[p] = 0
    res = _fill_shape(res)

    return res


class BrightnessMask(object):
    """
    Adjust image brightness.
    This class can be used to control the brightness of an image.  An
    enhancement factor of 0.0 gives a black image. A factor of 1.0 gives the
    original image.
    """

    def __init__(self, image, mask):
        self.image = image
        self.mask = mask
        color = choice(['white', 'black'])
        self.degenerate = Image.new(image.mode, image.size, color)
        if 'A' in image.getbands():
            self.degenerate.putalpha(image.getchannel('A'))

    def enhance(self, factor):
        mask = self.mask * factor
        mask = Image.fromarray(mask.astype('uint8'), mode='L')

        return Image.composite(self.degenerate, self.image, mask)
