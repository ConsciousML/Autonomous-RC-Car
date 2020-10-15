from layers.layer import Layer

from tqdm import tqdm
from PIL import Image

import os
from random import randint, shuffle


class Background(Layer):
    '''This layer is an input layer.
    It generates the inputs from background images.
    '''

    def __init__(self, n_backgrounds, path, n_rot=1, n_res=1, n_crop=1,
                    input_size=(250, 200), output_size=(250, 70),
                    width_range=None, angle_max=20, name='Background'):
        """

        Arguments:
            n_backgrounds: An integer,
                the number of backgrounds.
            path: A string,
                the path to the folder where background images
                are stocked.
            n_rot: A > 0 integer,
                the number of backgrounds to generate
                by rotating the existing background.
            n_res: A > 0 integer,
                the number of backgrounds to generate
                by resizing the existing background.
            n_crop: A > 0 integer,
                the number of backgrounds to generate
                by cropping the existing background.
            input_size:

            output_size:

            width_range:

            angle_max:

            name: a string,
                the name of the layer
        """

        # TODO: how to decrease the amount of ValueError ?
        # TODO: how to increase readibility ?
        if width_range is None:
            width_range = [i for i in range(output_size[0], output_size[0] + 500)]
        if name is None:
            raise ValueError('name must be different from None')
        if not isinstance(n_backgrounds, int):
            raise ValueError('The number of backgrounds to generate must be an integer')
        if n_backgrounds <= 0:
            raise ValueError('The number of backgrounds to generate must be positive')
        if not os.path.exists(path):
            raise ValueError('The path `{}` does not exist'.format(path))
        if not os.path.isdir(path):
            raise ValueError('The path `{}` is not a directory'.format(path))
        if len(os.listdir(path)) == 0:
            raise ValueError('There are no images at path `{}`'.format(path))
        if not all([isinstance(item, int) and item >= 0 for item in [n_rot, n_res, n_crop]]):
            raise ValueError('The number of rotations, resizing and cropping must all be positive. Not `{}`'.format(str([n_rot, n_res, n_crop])))
        if not isinstance(input_size, tuple):
            raise ValueError('input_size must be a tuple : `{}`'.format(str(input_size)))
        if not (len(input_size) == 2):
            raise ValueError('input_size must be 2 dimensional: `{}`'.format(len(input_size)))
        if not (isinstance(input_size[0], int) and isinstance(input_size[1], int) and input_size[0] >= 0 and input_size[1] >= 0):
            raise ValueError('input_size must be 2 dimensional: `{}`'.format(len(input_size)))
        if not isinstance(width_range, list) or len(width_range) == 0:
            raise ValueError('width_range must be a non-empty list or None')
        if max(width_range) < input_size[0]:
            # Because resizing during generation needs to be done on a higher
            # width
            # TODO: not a good test
            raise ValueError('TODO')

        super(Background, self).__init__()

        self.n_backgrounds = n_backgrounds
        self.path = path
        self.n_rot = n_rot
        self.n_res = n_res
        self.n_crop = n_crop
        self.input_size = input_size
        self.width_range = width_range
        angle_max = angle_max % 360
        self.angles_range = [i for i in range(0, angle_max)] + [i for i in range(360-angle_max, 360)] + [i for i in range(180-angle_max, 180+angle_max)]
        self.backgrounds = self.generate_all_backgrounds()

        self.name = name

    def generate_all_backgrounds(self):
        """Generates backgrounds via:
            - choice of background image
            - rotation
            - resizing
            - cropping

        Returns:
            List of images of backgrounds.
        """

        width, height = self.input_size

        # Choice of the background image
        backgrounds = []
        image_names = os.listdir(self.path)
        n = min([len(image_names), self.n_backgrounds])
        for index in tqdm(range(n), desc='loading images'):
            background = Image.open(os.path.join(self.path, image_names[index])).convert('RGB')
            backgrounds.append(background)


        # Generation of the resized images
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='resizing images'):
            for _ in range(self.n_res):
                b = backgrounds[i]
                # Choice of the resize size
                index = randint(0, len(self.width_range)-1)
                new_width = self.width_range[index]
                new_height = int(4 * new_width / 5)
                b = b.resize((new_width, new_height), Image.ANTIALIAS)
                new_backgrounds.append(b)

        # Generation of the rotations
        backgrounds = new_backgrounds
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='rotating images'):
            background = backgrounds[i]
            for j in range(self.n_rot):
                b = background.copy()
                # Choice of a rotation angle
                angle_rotation = self.angles_range[randint(0, len(self.angles_range)-1)]
                b = b.rotate(angle_rotation)
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        if len(backgrounds) >= self.n_backgrounds:
            shuffle(backgrounds)
            backgrounds = backgrounds[:self.n_backgrounds]

        backgrounds = new_backgrounds
        if len(backgrounds) >= self.n_backgrounds:
            shuffle(backgrounds)
            backgrounds = backgrounds[:self.n_backgrounds]

        # Generation of the cropped images
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='cropping images'):
            background = backgrounds[i]
            for j in range(self.n_crop):
                b = background.copy()
                # Choice of the rectangle to crop
                x0, y0 = randint(0, b.width - width), randint(0, b.height - height)
                x1, y1 = x0 + width, y0 + height
                b = b.crop((x0, y0, x1, y1))
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        shuffle(backgrounds)
        backgrounds = backgrounds[:self.n_backgrounds]

        return backgrounds

    def summary(self):
        """Returns a string describing the layer"""

        return '{}\t{}\t{}\t{}\t{}'.format(self.name, self.n_backgrounds,
                                            self.n_res, self.n_rot, self.n_crop)
