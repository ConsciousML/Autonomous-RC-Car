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

# Flags
PRINT_TIME = True
ULTRASONIC = True

# Obstacle Detection
sleep_time = 0.3
if ULTRASONIC:
    ultrason = ultrasonic.UltrasonicAsync(sleep_time)
    ultrason.start()
    obstacleExist = False


# To be imported from externals
def bin_array(numpy_array, threshold=160):
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
motor.setSpeed(50)
motor.forward()
video_dir.home_x_y()
car_dir.home()

# Load classifier
CLF_FOLDER = "../"
CLF_NAME = "forest_recurent_same_nb"
clf = joblib.load(CLF_FOLDER + CLF_NAME + ".joblib.pkl")

labels = ['forward', 'left', 'right']
rev_labels = {'forward':0, 'left':1, 'right':2 }
ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

# Component initialization
cam = cv2.VideoCapture(0)
print("ok")

i = 0
while True:
    data = ''
    last_data = None
    last_img = None

    # Check of obstacles
    if ULTRASONIC:
        print '%2d: check if obstacle' % i
        if ultrason.dist < 100:
            print '*** Found new obstacle at distance %f' % ultrason.dist
            motor.stop()
            obstacleExist = True

        while obstacleExist:
            time.sleep(sleep_time)
            if ultrason.dist < 100:
                print 'Can not move. Obstacle is at distance %f' % ultrason.dist
            else:
                print '*** Can move! Obstacle is now at distance %f' % ultrason.dist
                obstacleExist = False
                motor.forward()

    try:
        print '%2d: read image' % i

        # Take input from camera
        if PRINT_TIME:
            t_init = time.time()
        ret, frame = cam.read()
        if PRINT_TIME:
            t_imread = time.time()
            print 'imread took %0.3f s' % (t_imread - t_init)
            t_init = time.time()

        if ret:
            # Preprocess the image
            img = imresize(frame, (80, 60))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = bin_array(img)
            img = img.reshape(1, -1) # because it is a single feature

            # Build recurrent programming
            sample = np.ones((1, 80 * 60 + 1))
            if last_img is None:
                sample = np.append(img,  img)
                sample = np.append(sample, rev_labels['forward']) # because what else?
            else:
                sample = np.append(img, last_img)
                sample = np.append(sample, rev_labels[last_data])

            # Predict
            if PRINT_TIME:
                t_process = time.time()
                print 'image process took %0.3f s' % (t_process - t_init)
                t_init = time.time()

            sample = sample.reshape(1, -1) # because it is a single feature
            data = clf.predict(sample)
            if PRINT_TIME:
                t_pred = time.time()
                print 'prediction took %0.3f s' % (t_pred - t_init)

            data = labels[int(data[0])]
            print '%2d: prediction: %s' % (i, data)

            # Update recurrent
            last_img = img
            last_data = data

        else:
            print "*** Problems taking a picture."
        i += 1
    except:
        print '*** Exception'
        if ULTRASONIC:
            ultrason.stop()
            ultrason.join()
        cam.release()
        motor.stop()
        raise

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
