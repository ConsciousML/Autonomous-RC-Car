class Layer():
    '''Root Object of Layer.
    By default, identity layer.
    '''

    def __init__(self, name='Layer'):
        if name is None: raise ValueError('name must be different from None')
        self.name = name

    def call(self, img):
        if img is None: raise ValueError('img is None')
        return img

    def summary(self):
        return self.name
