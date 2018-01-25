import numpy as np
import cv2
import glob

offset = 4
ki = 0

for filef in glob.glob("fake/*.jpg"):
    try:

        img = cv2.imread(filef, 1)
        imgs = cv2.imread(filef, 1)

        imgh = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lowerl_red = np.array([0,0,0])
        upperl_red = np.array([17,255,255])


        loweru_red = np.array([153,0,0])
        upperu_red = np.array([179,255,255])

        mask1 = cv2.inRange(imgh, lowerl_red, upperl_red)
        mask2 = cv2.inRange(imgh, loweru_red, upperu_red)

        img = cv2.bitwise_and(img,img, mask = mask1 | mask2)
        simg = img

        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _,thresh = cv2.threshold(img,1,255,cv2.THRESH_BINARY)

        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except:
        continue

    for i in range(len(contours)):
        cnt = contours[i]
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        x = int(x)
        y = int(y)
        radius = int(radius)
        print(i, x, y, radius)
        if radius > 10 and radius < 50:
            try:
                img2 = imgs[y - offset - radius : y + radius + offset, x - radius - offset : x + radius + offset]
                if img2.shape[0] > 0 and img2.shape[1] > 0 and img2.shape[2] == 3:
                    cv2.imwrite("detect/" + str(ki) + ".jpg", img2)
                ki += 1
            except:
                continue
