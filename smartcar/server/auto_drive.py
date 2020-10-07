#!/usr/bin/env python
import sys
import video_dir
import car_dir
import motor
import cv2
import numpy
import RPi.GPIO as GPIO
import numpy as np
import numpy as np
import time
from time import sleep
from socket import *
from sklearn.externals import joblib
from PIL import Image
from scipy.misc import imsave
from scipy.misc import imresize
from keras.models import load_model
from picamera.array import PiRGBArray
from picamera import PiCamera

import ultrasonic
import threading
import sign_classification

"""

This files contains all the logic on the autonomous driving.
It loads the driving model predicts the angle and speed from
the camera image in real-time. The car also stops if it 
detects a stop sign or if there is an obstacle.


"""


if __name__ == '__main__':
    # Obstacle Detection
    sleep_time = 0.3
    GPIO.setmode(GPIO.BOARD)

    # Settings initialization
    busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0
    video_dir.setup(busnum=busnum)
    car_dir.setup(busnum=busnum)
    motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
    motor.setSpeed(50)
    video_dir.home_x_y()
    car_dir.home()

    motor.ctrl(0)

    # Load classifier

    model_path = os.path.join('..', '..', 'models', 'model_aug_bright.h5')
    model = load_model(model_path)

    ctrl_cmd = ['forward',
                'backward',
                'left',
                'right',
                'stop',
                'read cpu_temp',
                'home',
                'distance',
                'x+',
                'x-',
                'y+',
                'y-',
                'xy_home']

    # Component initialization
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.hflip = True
    cam.vflip = True

    i = 0

    output_full = None
    stop_detected = False
    lstop_detected = False

    class SignsThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.model = load_model(os.path.join('..', '..', 'models', 'sign_classification')

        def run(self):
            while True:
                if output_full is not None:
                    global stop_detected
                    global lstop_detected
                    stop_detected = self.model.predict(output_full)
                    if stop_detected:
                        sleep(1)
                        lstop_detected = True
                        stop_detected = False
                        sleep(1)

    threadss = SignsThread()
    threadss.start()

    time.sleep(2)

    ultrason = ultrasonic.UltrasonicAsync(sleep_time)
    ultrason.start()
    obstacleExist = False

    motor.forward()

    while True:
        data = ''

        # Check of obstacles
        if ultrason.dist < 20:
            motor.ctrl(0)
            obstacleExist = True

        while obstacleExist:
            time.sleep(sleep_time)
            if ultrason.dist < 20:
                obstacleExist = False
                motor.forward()

        # Take input from camera
        output_full2 = np.empty(480 * 640 * 3, dtype=np.uint8)
        cam.capture(output_full2, 'bgr', use_video_port=True)

        output_full = output_full2.reshape((480, 640, 3))
        crop_idx = int(output_full.shape[0] / 2)
        output = output_full[crop_idx:, :]

        img_detection = imresize(output, (120, 160))

        pred = model.predict(img_detection.reshape((1, 120, 160, 3)))
        speed_pred = pred[1][0][0]
        motor.setSpeed(int(speed_pred * 62 + 40))
        pred = pred[0][0][0]

        i += 1

        data = ctrl_cmd[0]
        if stop_detected:
            data = ctrl_cmd[4]
        elif pred < 0.03 and pred > -0.03:
            data = ctrl_cmd[6]
        else:
            angle = int((pred / 2 + 0.5) * 170 + 35)
            data = "turn=" + str(angle)

        if lstop_detected:
            motor.forward()
            lstop_detected = False

        if data == ctrl_cmd[0]:
            print 'motor moving forward'
            motor.forward()
        elif data == ctrl_cmd[1]:
            print 'recv backward cmd'
            motor.backward()
        elif data == ctrl_cmd[2]:
            print 'recv left cmd'
            car_dir.turn_left()
        elif data == ctrl_cmd[3]:
            print 'recv right cmd'
            car_dir.turn_right()
        elif data == ctrl_cmd[6]:
            print 'recv home cmd'
            car_dir.home()
        elif data == ctrl_cmd[4]:
            print 'recv stop cmd'
            motor.ctrl(0)
        elif data == ctrl_cmd[5]:
            print 'read cpu temp...'
            temp = cpu_temp.read()
        elif data == ctrl_cmd[8]:
            print 'recv x+ cmd'
            video_dir.move_increase_x()
        elif data == ctrl_cmd[9]:
            print 'recv x- cmd'
            video_dir.move_decrease_x()
        elif data == ctrl_cmd[10]:
            print 'recv y+ cmd'
            video_dir.move_increase_y()
        elif data == ctrl_cmd[11]:
            print 'recv y- cmd'
            video_dir.move_decrease_y()
        elif data == ctrl_cmd[12]:
            print 'home_x_y'
            video_dir.home_x_y()
        elif data[0:5] == 'speed':     # Change the speed
            print data
            numLen = len(data) - len('speed')
            if numLen == 1 or numLen == 2 or numLen == 3:
                tmp = data[-numLen:]
                print 'tmp(str) = %s' % tmp
                spd = int(tmp)
                print 'spd(int) = %d' % spd
                if spd < 24:
                    spd = 24
                motor.setSpeed(spd)
        elif data[0:5] == 'turn=':	#Turning Angle
            print 'data =', data
            angle = data.split('=')[1]
            try:
                angle = int(angle)
                car_dir.turn(angle)
            except:
                print 'Error: angle =', angle
        elif data[0:8] == 'forward=':
            print 'data =', data
            spd = data[8:]
            try:
                spd = int(spd)
                motor.forward(spd)
            except:
                print 'Error speed =', spd
        elif data[0:9] == 'backward=':
            print 'data =', data
            spd = data.split('=')[1]
            try:
                spd = int(spd)
                motor.backward(spd)
            except:
                print 'ERROR, speed =', spd

        else:
            print 'Command Error! Cannot recognize command: ' + data

    # Proper thread kill
    ultrason.stop()
    ultrason.join()
