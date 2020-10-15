from layers import Layer


class Noise(Layer):

    '''
        Root Object of Noise.
        By default, identity layer.
    '''

    def __init__(self, name='Noise'):
        if name is None:
            raise ValueError('')
        self.name = name

    def call(self, img):
        if img is None:
            raise ValueError('img is None')
        return img

    def summary(self):
        return self.name