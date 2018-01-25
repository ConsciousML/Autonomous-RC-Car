import numpy as np
import cv2

offset = 9

img = cv2.imread('test11.jpg', 1)
imgs = cv2.imread('test11.jpg', 1)

imgh = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lowerl_red = np.array([0,40,40])
upperl_red = np.array([10,255,255])


loweru_red = np.array([160,40,40])
upperu_red = np.array([179,255,255])

mask1 = cv2.inRange(imgh, lowerl_red, upperl_red)
mask2 = cv2.inRange(imgh, loweru_red, upperu_red)

img = cv2.bitwise_and(img,img, mask = mask1 | mask2)
simg = img

img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_,thresh = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
cv2.imshow("cropped", thresh)
cv2.waitKey(0)

_, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    cnt = contours[i]
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    print(i, x, y, radius)
    if radius > 10:
        img2 = imgs[y - offset - radius : y + radius + offset, x - radius - offset : x + radius + offset]

        cv2.imshow("cropped", img2)
        cv2.waitKey(0)

'''circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 3.5 , 100, param1=30,param2=40,minRadius=15,maxRadius=50)

count = 0


if circles is not None:
  # convert the (x, y) coordinates and radius of the circles to integers
  circles = np.round(circles[0, :]).astype("int")

  # loop over the (x, y) coordinates and radius of the circles
  for (x, y, r) in circles:
    count += 1
    # draw the circle in the output image, then draw a rectangle
    # corresponding to the center of the circle
#    img = cv2.imread('test11.jpg', 1)
    cv2.circle(img, (x, y), r, (0, 255, 0), 4)
    cv2.rectangle(simg, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    crop_img = img[y-r-offset:y+r+offset, x-r-offset:x+r+offset]

    cv2.imshow("cropped", img)
    cv2.waitKey(0)

print(count)
cv2.destroyAllWindows()'''
