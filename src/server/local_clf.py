#!/usr/bin/env python
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

import ultrasonic

# To be imported from externals
def bin_array(numpy_array, threshold=170):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

# Settings initialization
busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0
video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
video_dir.home_x_y()
car_dir.home()

# Load classifier
CLF_FOLDER = "../"
CLF_NAME = "forest_defaultparams"
clf = joblib.load(CLF_FOLDER + CLF_NAME + ".joblib.pkl")

labels = ['forward', 'left', 'right']
ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

# Component initialization
cam = cv2.VideoCapture(0)
sleep_time = 0.3

# Flags
PRINT_TIME = False
ULTRASONIC = False


# Obstacle Detection
if ULTRASONIC:
    ultrason = ultrasonic.UltrasonicAsync(sleep_time)
    ultrason.run()
    obstacleExist = False

i = 0
while True:
    data = ''

    # Check of obstacles
    if ULTRASONIC:
        print '%2d: check if obstacle' % i
        if ultrason.dist < 100:
            print '*** Found new obstacle at distance %f' % ultrason.dist
            obstacleExist = True
    
        while obstacleExist:
            time.sleep(sleep_time)
            if ultra.dist < 100:
                print 'Can not move. Obstacle is at distance %f' % ultrason.dist
            else:
                print '*** Can move! Obstacle is now at distance %f' % ultrason.dist
                obstacleExist = False

    try:
        print '%2d: read image' % i

        if PRINT_TIME:
            t_init = time.time()
        ret, frame = cam.read()
        if PRINT_TIME:
            t_imread = time.time()
            print 'imread took %0.3f s' % (t_imread - t_init)
            t_init = time.time()

        if ret:
            img = imresize(frame, (80, 60))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = bin_array(img)
            img = img.reshape(1, -1) # because it is a single feature
            if PRINT_TIME:
                t_process = time.time()
                print 'image process took %0.3f s' % (t_process - t_init)
                t_init = time.time()

            data = clf.predict(img)
            if PRINT_TIME:
                t_pred = time.time()
                print 'prediction took %0.3f s' % (t_pred - t_init)

            data = labels[int(data[0])]
            print '%2d: prediction: %s' % (i, data)

        else:
            print "*** Problems taking a picture."
        i += 1
    except:
        print '*** Exception'
        pass

    # Analyze the command received and control the car accordingly.
    if not data:
        break

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

cam.release()

# Proper thread kill
if ULTRASONIC:
    ultrason.stop()
    ultrason.join()
