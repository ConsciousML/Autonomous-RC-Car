from layers import Layer
from utils import find_coeffs

from PIL import Image

from random import random


class Symmetric(Layer):
    '''This layer creates the symmetric of an image.'''

    def __init__(self, proba=0.5, name='Symmetric'):
        """
        Arguments:
            proba: A float,
                the probability to use the symmetric instead of the original
                image. On the original image, the lines are always going to
                the right.

            name: A string,
                the name of the layer
        """

        super(Symmetric, self).__init__()

        if name is None:
            raise ValueError('name must be different from None')
        if proba is None or not (isinstance(proba, float) or isinstance(proba, int)) or not (0 <= proba <= 1):
            raise ValueError('The probability must be a float or integer and 0 <= proba <= 1')

        self.proba = proba
        self.name = name

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        width, height = img.size
        sym = img.copy()

        symmetry = False
        if random() < self.proba:
            from_points = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]
            new_points = [(width-1, 0), (0, 0), (0, height-1), (width-1, height-1)]
            coeffs = find_coeffs(new_points, from_points)
            # Symmetry according to PIL..
            sym = sym.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
            symmetry = True
        return sym, symmetry

    def summary(self):
        """Returns a string describing this layer"""

        return '{}\t{}'.format(self.name, self.proba)

