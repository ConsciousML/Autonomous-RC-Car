from keras.models import load_model
from keras.applications.mobilenet import preprocess_input
import numpy as np
import cv2

sign_model = load_model("../../models/sign_classification.h5")
i = 0

def predict(imgrgb):
    print "Lauching predictions"
    offset = 9

    img = imgrgb
    imgs = imgrgb
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

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        if radius > 10:
            x,y,w,h = cv2.boundingRect(cnt)
            img2 = imgs[y - offset : y + h + offset, x - offset : x + w + offset]
            try:
                crop_img = cv2.resize(img2, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
                lab = sign_model.predict(preprocess_input(crop_img.astype(float)).reshape((1, 32, 32, 3)))
                if lab[0][1] > 0.5:
                    i += 1
                    cv2.imwrite('img' + str(i) + '.png', imgs)
                    cv2.imwrite('false_detect' + str(i) + '.png', crop_img)
                    return True
            except:
                continue
    return False
