import numpy as np
import scipy
from scipy.ndimage.filters import gaussian_filter
import cv2
import filters

sigma = 0.33
filename = "pictures/104forward.jpg"
#img = cv2.imread(filename)
#(thresh, img_bin) = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
img_bin = filters.binarize(filename)
v = np.median(img_bin)
lo = int(max(0, (1.0 - sigma) * v))
up = int(max(255, (1.0 + sigma) * v))

canny_img = cv2.Canny(img_bin, lo, up)
scipy.misc.imsave("canny_test.jpg", canny_img)
