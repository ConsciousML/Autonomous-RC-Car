from keras.models import load_model
from keras.applications.mobilenet import preprocess_input
import numpy as np
import cv2

sign_model = load_model("../../models/sign_classification.h5")
sign_model._make_predict_function()

i = 0

def predict(imgrgb):
    offset = 4

    img = imgrgb
    imgs = imgrgb
    imgh = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lowerl_red = np.array([11,150,150])
    upperl_red = np.array([20,255,255])

    mask1 = cv2.inRange(imgh, lowerl_red, upperl_red)

    img = cv2.bitwise_and(img,img, mask = mask1)
    simg = img

    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(img,1,255,cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        x = int(x)
        y = int(y)
        radius = int(radius)
        if radius > 5 and radius < 20:
#           x,y,w,h = cv2.boundingRect(cnt)
#           img2 = imgs[y - offset - radius : y + radius + offset, x - offset - radius : x + radius + offset]
            
#            if (img2.shape[0] > 0 and img2.shape[1] > 0 and img2.shape[2] == 3):
#                crop_img = cv2.resize(img2, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
#                lab = sign_model.predict(preprocess_input(crop_img.astype(float)).reshape((1, 32, 32, 3)))
#                if lab[0][1] > 0.5:
#                    i += 1
            return True
    return False
