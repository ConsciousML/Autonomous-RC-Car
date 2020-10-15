from layers.noises.noise import Noise

from PIL import ImageEnhance

from random import randint, random


class Enhance(Noise):

    '''
        Adds enhancements filters to the image.
    '''

    def __init__(self, contrast=0, brightness=0, sharpness=0, color=0, name='Enhance'):

        if name is None:
            raise ValueError()
        if not all([item is not None and (isinstance(item, float) or isinstance(item, int)) for item in [contrast, brightness, sharpness, color]]):
            raise ValueError
        if sum([contrast, brightness, sharpness, color]) > 1:
            raise ValueError
        if not all(0 <= item <= 1 for item in [contrast, brightness, sharpness, color]):
            raise ValueError
        super(Enhance, self).__init__()
        self.name = name

        self.contrast = contrast
        self.brightness = brightness
        self.sharpness = sharpness
        self.color = color

    def call(self, img):

        if img is None: raise ValueError('img is None')

        im_n = img.copy()

        r = random()
        contrast_low, contrast_high = 0, self.contrast
        brightness_low, brightness_high = contrast_high, contrast_high + self.brightness
        sharpness_low, sharpness_high = brightness_high, brightness_high + self.sharpness
        color_low, color_high = sharpness_high, sharpness_high + self.color

        if contrast_low <= r < contrast_high:
            factor_contrast = randint(5, 10)/10
            enhancer = ImageEnhance.Contrast(im_n)
            im_n = enhancer.enhance(factor_contrast)
        elif brightness_low <= r < brightness_high:
            factor_brightness = randint(5, 15) / 10
            enhancer = ImageEnhance.Brightness(im_n)
            im_n = enhancer.enhance(factor_brightness)
        elif sharpness_low <= r < sharpness_high:
            factor_sharpen = randint(0, 20)/10
            enhancer = ImageEnhance.Sharpness(im_n)
            im_n = enhancer.enhance(factor_sharpen)
        elif color_low <= r < color_high:
            factor_color = randint(0, 20)/10
            enhancer = ImageEnhance.Color(im_n)
            im_n = enhancer.enhance(factor_color)
        else:
            pass

        return im_n
