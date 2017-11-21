import numpy as np
import cv2
from matplotlib import pyplot as plt
stop_cascade = cv2.CascadeClassifier('class/cascade.xml')

img = cv2.imread('test4.jpg')
img = cv2.resize(img, (640, 480))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = stop_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
  value = 0
  for i in range(x, x+w):
    for j in range(y, y+h):
        r = img[j, i, 2].astype(float) / np.sum(img[j, i, :])
        if r > 0.5 and img[j, i, 2] > 110:
            value += 1

  rat = float(value) / (w * h)
  print(rat)
  if rat > 0.15:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
