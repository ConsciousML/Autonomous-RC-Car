import numpy as np
import cv2
from matplotlib import pyplot as plt
stop_cascade = cv2.CascadeClassifier('class/cascade.xml')

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = stop_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
  mask = np.zeros(img.shape[:2], np.uint8)
  mask[y:y+h, x:x+w] = 255
  hist = cv2.calcHist([img],[2],mask,[256],[0,256])
  rat = np.sum(hist[200:]) / (w * h)
  print(rat)
  if rat > 0.1:
    plt.plot(hist)
    plt.xlim([0,256])
    plt.show()
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
