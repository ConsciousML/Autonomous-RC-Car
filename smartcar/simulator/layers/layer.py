class Layer():
    '''The layer class, each layer is a transformation

    By default, identity layer.

    '''

    def __init__(self, name='Layer'):
        """Sets the layer name"""
        if name is None: raise ValueError('name must be different from None')
        self.name = name

    def call(self, img):
        """Returns an image"""
        if img is None: raise ValueError('img is None')
        return img

    def summary(self):
        """Returns the name of the layer"""
        return self.name
