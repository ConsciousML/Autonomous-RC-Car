import os
import cv2

"""

This file contains functions that perform a vertical flip on images
as well as flipping the angle label to augment the training data

"""


def flip_angle(label):
    """Return the inverse angle of the input"""
    if (label >= 125):
        diff = label - 125
        return 125 - diff
    else:
        diff = 125 - label
        return 125 + diff


def flip_image(image_path, label):
    """Returns a verticaly flipped image as well as the inverse angle of the input
    
    Args:
        image_path: A string for the absolute path of the image.
        label: A float for the angle associated with the image.
    """
    image = cv2.imread(image_path, 1)
    image = cv2.flip(image, 1)
    return image, flip_angle(label)


