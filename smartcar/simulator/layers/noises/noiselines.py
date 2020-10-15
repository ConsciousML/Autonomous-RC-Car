from layers.noises.noise import Noise

from PIL import ImageDraw

from random import choice, randint, random


class NoiseLines(Noise):

    '''
        Adds noise lines to the image i.e. lines randomly on the picture.
    '''

    def __init__(self, color_range, n_lines_max=1, proba_line=0.33, name='NoiseLines'):

        if name is None:
            raise ValueError('')
        if color_range is None:
            raise ValueError
        if len(color_range.colors) == 0:
            raise ValueError
        if (not isinstance(n_lines_max, int)) or n_lines_max < 0:
            raise ValueError
        if not (isinstance(proba_line, float) or isinstance(proba_line, int)) or not 0 <= proba_line <= 1:
            raise ValueError

        super(NoiseLines, self).__init__()

        self.color_range = color_range
        self.n_lines_max = n_lines_max
        self.proba_line = proba_line

        self.name = name


    def call(self, img):

        def draw_line_dep(im, x1, y1, x2, y2, fill, width=1):
            draw = ImageDraw.Draw(im)
            draw.line((x1, y1, x2, y2), fill=fill, width=width)
            del draw
            return im

        if img is None: raise ValueError('img is None')

        n = randint(0, self.n_lines_max)
        for _ in range(n):
            if random() > self.proba_line: continue
            x1 = randint(0, img.width)
            x2 = randint(0, img.width)
            y1 = randint(0, img.height)
            y2 = randint(0, img.height)
            width = randint(1, 10)
            fill = choice(self.color_range.colors)
            img = draw_line_dep(img, x1, y1, x2, y2, fill, width=width)

        return img
