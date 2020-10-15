from layers.noises.noise import Noise

from PIL import ImageFilter

from random import random


class Filter(Noise):

    '''
        Adds filters to the image.
    '''

    def __init__(self, blur=0, gauss_blur=0, smooth=0, smooth_more=0, rank_filter=0, name='Filter'):
        if name is None:
            raise ValueError
        if not all([item is not None for item in [blur, gauss_blur, smooth, smooth_more, rank_filter]]):
            raise ValueError
        if blur + gauss_blur + smooth + smooth_more + rank_filter > 1:
            raise ValueError
        if not all(0 <= item <= 1 for item in [blur, gauss_blur, smooth, smooth_more, rank_filter]):
            raise ValueError

        super(Filter, self).__init__()

        self.blur = blur
        self.gauss_blur = gauss_blur
        self.smooth = smooth
        self.smooth_more = smooth_more
        self.rank_filter = rank_filter

        self.name = name

    def call(self, img):

        if img is None: raise ValueError('img is None')

        im_n = img.copy()

        gauss_blur_low, gauss_blur_high = 0, self.gauss_blur
        blur_low, blur_high = gauss_blur_high, gauss_blur_high + self.blur
        smooth_low, smooth_high = blur_high, blur_high + self.smooth
        smooth_more_low, smooth_more_high = smooth_high, smooth_high + self.smooth_more
        rank_low, rank_high = smooth_more_high, smooth_more_high + self.rank_filter

        r = random()
        if gauss_blur_low <= r <= gauss_blur_high:
            im_n = im_n.filter(ImageFilter.GaussianBlur(1))
        elif blur_low < r <= blur_high:
            im_n = im_n.filter(ImageFilter.BLUR)
        elif smooth_low < r <= smooth_high:
            im_n = im_n.filter(ImageFilter.SMOOTH)
        elif smooth_more_low < r <= smooth_more_high:
            im_n = im_n.filter(ImageFilter.SMOOTH_MORE)
        elif rank_low < r <= rank_high:
            im_n = im_n.filter(ImageFilter.RankFilter(size=3, rank=7))
        else:
            pass
        return im_n