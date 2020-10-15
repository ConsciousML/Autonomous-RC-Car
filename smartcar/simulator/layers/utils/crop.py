from layers import Layer


class Crop(Layer):
    '''This layer crops the image.'''

    def __init__(self, output_dim=(250, 70), name='Crop'):
        """
        Arguments:
            output_dim: A tuple of 2-integers, (width, height),
                the output dimensions of the image after crop.

            name: A string,
                the name of the layer
        """

        if name is None:
            raise ValueError('name must be different from None')

        super(Crop, self).__init__()

        self.new_width = output_dim[0]
        self.new_height = output_dim[1]
        self.name = name

    def call(self, img):
        if img is None: raise ValueError('img is None')

        width = img.width

        x_shift = self.new_width

        img = img.crop((x_shift-1, 0, width-x_shift-1, self.new_height))

        return img
