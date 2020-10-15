from layers.noises import Noise
from utils.image_operations import BrightnessMask, generate_shape

from random import randint, random


class Shape(Noise):

    """
        Adds shape filters to the image.
    """

    def __init__(self, brightness=0, name='Shape'):

        if name is None:
            raise ValueError()
        if not all([item is not None and (isinstance(item, float) or isinstance(item, int)) for item in [brightness]]):
            raise ValueError
        if sum([brightness]) > 1:
            raise ValueError
        if not all(0 <= item <= 1 for item in [brightness]):
            raise ValueError
        super(Shape, self).__init__()
        self.name = name

        self.brightness = brightness

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        im_n = img.copy()
        width, height = img.size

        r = random()
        brightness_low, brightness_high = 0, self.brightness

        if brightness_low <= r < brightness_high:
            factor_brightness = randint(175, 176)
            mask = generate_shape((height, width, 3))[:, :, 0]
            enhancer = BrightnessMask(im_n, mask)
            im_n = enhancer.enhance(factor_brightness)
        else:
            pass

        return im_n
