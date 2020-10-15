from layers.noises.noise import Noise

from PIL import ImageDraw

from random import choice, randint


class Shadows(Noise):

    '''
        Adds shadows to the image.
    '''

    def __init__(self, colors=None, name='Shadows'):

        if name is None:
            raise ValueError('')
        if colors is None:
            raise ValueError('')

        super(Shadows, self).__init__()

        self.colors = colors
        self.name = name

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        x1 = randint(0, img.width)
        x2 = randint(0, img.width)
        y1 = randint(0, img.height)
        y2 = 10000000
        color_range = choice(self.colors)
        c = choice(color_range.colors)

        while abs(y2 - y1) > 75:
            if randint(0, 1):
                y2 = randint(y1, img.height)
            else:
                y2 = randint(0, y1)

        draw = ImageDraw.Draw(img)
        draw.rectangle((x1, y1, x2, y2), fill=c, outline=c)
        del draw

        return img