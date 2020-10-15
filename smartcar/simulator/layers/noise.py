'''
    Noise Layers are for now on just layers like the 'normal' layers.
'''

import PIL
import os
import sys
import numpy as np

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from math import sqrt, atan2, pi
from random import randint, shuffle, choice, gauss, random
from tqdm import tqdm

from basic_objects import Point, RoadLine, Circle

sys.path.insert(0, '../')
from layers import Layer






