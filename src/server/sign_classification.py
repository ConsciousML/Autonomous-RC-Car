from keras.models import load_model
from keras.applications.mobilenet import preprocess_input
import numpy as np
import cv2

sign_model = load_model("../../models/sign_classification.h5")

def predict(imgrgb):
    print "Lauching predictions"
    offset = 3

    img = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2GRAY)
    print img.shape
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.4 , 10, param1=130,param2=60,minRadius=0,maxRadius=0)

    count = 0

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            if r > 50:
                continue
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle

            try:
                crop_img = imgrgb[y-r-offset:y+r+offset, x-r-offset:x+r+offset]
                crop_img = cv2.resize(crop_img, dsize=(32, 32), interpolation=cv2.INTER_NEAREST)
                print count
                lab = sign_model.predict(preprocess_input(crop_img.astype(float)).reshape((1, 32, 32, 3)))
                if lab[0][1] > 0.5:
                    return True
                count += 1
            except:
                continue
    return False
