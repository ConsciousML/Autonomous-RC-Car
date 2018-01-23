#!/usr/bin/env python
import sys

import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import cv2
import numpy
from socket import *
from sklearn.externals import joblib
import numpy as np
from PIL import Image
from scipy.misc import imsave
from scipy.misc import imresize
import numpy as np
import time
from keras.models import load_model
from picamera.array import PiRGBArray
from picamera import PiCamera

import sign_classification

import ultrasonic

# Flags
ULTRASONIC = False
STOP = False

# Obstacle Detection
sleep_time = 0.3
if ULTRASONIC:
    ultrason = ultrasonic.UltrasonicAsync(sleep_time)
    ultrason.start()
    obstacleExist = False

GPIO.setmode(GPIO.BOARD)

# Settings initialization
busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0
video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
motor.setSpeed(50)
video_dir.home_x_y()
car_dir.home()

# Load classifier

using_keras = True
if using_keras:
    CLF_FOLDER = "../../models/"
    CLF_NAME = "speed_model.h5"
    clf = load_model(CLF_FOLDER + CLF_NAME)
    print("Classifier loaded")
else:
    CLF_FOLDER = "../"
    CLF_NAME = "forest_recurent_same_nb.joblib.pkl"
    clf = joblib.load(CLF_FOLDER + CLF_NAME)

labels = ['forward', 'left', 'right']
rev_labels = {'forward':0, 'left':1, 'right':2 }
ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

# Component initialization
cam = PiCamera()
cam.resolution = (640, 480)
cam.hflip = True
cam.vflip = True

time.sleep(2)

i = 0

#motor.forward()

while True:
    data = ''
    last_data = None
    last_img = None
    stop_detected = False
    obligation_detected = False
    last_stop_time = 0

    # Check of obstacles
    if ULTRASONIC:
        print '%2d: check if obstacle' % i
        if ultrason.dist < 60:
            print '*** Found new obstacle at distance %f' % ultrason.dist
            motor.ctrl(0)
            obstacleExist = True

        while obstacleExist:
            time.sleep(sleep_time)
            if ultrason.dist < 60:
                print 'Can not move. Obstacle is at distance %f' % ultrason.dist
            else:
                print '*** Can move! Obstacle is now at distance %f' % ultrason.dist
                obstacleExist = False
                motor.forward()

    try:
        # Take input from camera
        output_full = np.empty(480 * 640 * 3, dtype=np.uint8)
        cam.capture(output_full, 'bgr', use_video_port=True)

        output = output_full.reshape((480, 640, 3))
        crop_idx = int(output.shape[0] / 2)
        output = output[crop_idx:, :]

        img_detection = imresize(output, (120, 160))

        # Predict
        if STOP:
            stop_detected = sign_classification.predict(output_full)

        if using_keras:
            pred = clf.predict(img_detection.reshape((1, 120, 160, 3)))
            speed_pred = pred[1][0][0]
            motor.setSpeed(int(speed_pred * 62 + 40))
            pred = pred[0][0][0]

        print '%2d: prediction: %s' % (i, pred)

        i += 1
    except:
        print '*** Exception'
        motor.stop()
        if ULTRASONIC:
            ultrason.stop()
            ultrason.join()
        raise

    # Detection
    time_since_stop = time.time() - last_stop_time

    data = ctrl_cmd[0]
    if stop_detected:
        print 'Stop detected. Stopping...'
        data = ctrl_cmd[4]
        last_stop_time = time.time()
    else:
        if pred < 0.03 and pred > -0.03:
            data = ctrl_cmd[6]
        else:
            angle = int((pred / 2 + 0.5) * 170 + 35)
            data = "turn=" + str(angle)

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
if ULTRASONIC:
    ultrason.stop()
    ultrason.join()
