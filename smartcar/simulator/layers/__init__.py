'''All general layers objects.
A layer has 1 important functions: `call`. This is the function used to
manipulate the image that goes out of the former layer.

When you want to create a new layer on your own, you have to follow this
scheme:

    class MyLayer(Layer):

        def __init__(self, **args, **kwargs):
            # The constructor of the class
            ...

        def call(self, img):
            # Manipulate the img to do whatever the layer is supposed to do
            ...
            return img

        def summary():
            # Gives information about what is in this layer
            # Optional
            ...
'''

from .draw import Background, DrawLines
from .layer import Layer
from .utils import Crop, Perspective, Symmetric
