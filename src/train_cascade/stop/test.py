import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

stop_cascade = cv2.CascadeClassifier('class/cascade.xml')

def detect_stop(img, gray, verbose=False, show=False):
  faces = stop_cascade.detectMultiScale(gray, 1.3, 5)

  for (x,y,w,h) in faces:
    value = 0
    for i in range(x, x+w):
      for j in range(y, y+h):
          r = img[j, i, 2].astype(float) / np.sum(img[j, i, :])
          if r > 0.5 and img[j, i, 2] > 90:
              value += 1

    rat = float(value) / (w * h)
    if verbose:
      print(rat)
    if rat > 0.15:
      if show:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow(fname,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
      return True
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = img[y:y+h, x:x+w]

  return False

def detect_stop_from_file(fname, timer=False):
  img = cv2.imread(fname)
  img = cv2.resize(img, (640, 480))
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  if timer:
    start = time.time()
  stop_detected = detect_stop(img, gray)
  if timer:
    stop = time.time()
    diff = stop - start
    #print("{:.6f}s".format(diff))
    return diff
