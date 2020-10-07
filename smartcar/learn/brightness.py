import cv2
import numpy as np

"""

This file contains a function that randomly alters the brightness
of an input image to generate more data for training.

"""

def randomize_brightness(image):
    """Returns the same image as the input with an randomly altered brightness

    Args:
        image: An opencv image.
    """
    image_new = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    image_new = np.array(image_new, dtype=np.float64)
    random_bright = .5 + np.random.uniform()
    image_new[:, :, 2] = image_new[:, :, 2] * random_bright
    image_new[:, :, 2][image_new[:, :, 2] > 255]  = 255
    image_new = np.array(image_new, dtype=np.uint8)
    image_new = cv2.cvtColor(image_new, cv2.COLOR_HSV2RGB)
    return image_new