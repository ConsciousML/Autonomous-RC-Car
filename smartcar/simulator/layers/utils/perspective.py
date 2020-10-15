from layers import Layer 
from utils import find_coeffs

from PIL import Image


class Perspective(Layer):
    '''This layer creates the perspective of an image.'''

    def __init__(self, output_dim=(250, 70), name='Perspective'):
        """
        Arguments:
            output_dim: A tuple of 2-integers, (width, height),
                the output dimensions of the image after perspective.

            name: A string,
                the name of the layer
        """

        if name is None:
            raise ValueError('name must be different from None')

        super(Perspective, self).__init__()

        self.new_width = output_dim[0]
        self.new_height = output_dim[1]
        self.name = name

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        width, height = img.size
        from_points = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]
        new_points = [(self.new_width-1, 0),
                        (self.new_width+self.new_width-1, 0),
                        (self.new_width*2+self.new_width-1, self.new_height-1),
                        (0, self.new_height-1)]
        coeffs = find_coeffs(new_points, from_points)
        img = img.transform((self.new_width+self.new_width*2, self.new_height),
                                Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        return img