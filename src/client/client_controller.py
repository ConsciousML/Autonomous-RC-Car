#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *      # Import necessary modules
import numpy
import cv2
import os
import pickle
import scipy
import filters
import xbox
import math
import time
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import PIL


os.system('xset r off')
ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']


HOST = '192.168.43.46'    # Laure (Ionis's Down) IP address
HOST = '172.20.10.11'     # Thibaut (iPhone) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server
tcpCliSock.setblocking(1)

dira = 0

dic_dir = {-1: "left", 0: "forward", 1: "right"}
dic_dir_l = {1: "left", 0: "home", 2: "right"}

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

class Counter:
    i = 1437

def get_img(angle):
    global dira
    FOLDER = "pictures/"
    length = recvall(tcpCliSock, 16)
    stringData = recvall(tcpCliSock, int(length))
    img = numpy.fromstring(stringData, dtype='uint8')
    imgdec = cv2.imdecode(img, 1)
    path = FOLDER + str(Counter.i).zfill(3) + "_" + str(angle) + ".jpg"
    print path
    cv2.imwrite(path, imgdec)
    Counter.i += 1

'''
def get_image():
    img = tcpCliSock.recv()

top.bin("<<GetImg>>", get_image)
top.event_generate("<<GetImg>>", when="tail")
'''

def process_dir(dir):
    print dir
    tcpCliSock.send(dir)
    get_img(dir)

# =============================================================================
# The function is to send the command forward to the server, so as to make the
# car move forward.
# =============================================================================
def forward_fun(event):
    process_dir("forward")

def backward_fun(event):
    process_dir("backward")

def left_fun(event):
    global dira
    dira = -1
    process_dir("left")

def right_fun(event):
    global dira
    dira = 1
    process_dir("right")

def stop_fun(event):
    process_dir('stop')

def home_fun(event):
    global dira
    dira = 0
    process_dir('home')

def x_increase(event):
    process_dir('x+')

def x_decrease(event):
    process_dir('x-')

def y_increase(event):
    process_dir('y+')

def y_decrease(event):
    process_dir('y-')

def xy_home(event):
    process_dir('xy_home')

spd = 100

def changeSpeed():
    tmp = 'speed'
    global spd
    data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'.
    print 'sendData = %s' % data
    data = ajust_buffer(data)
    tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)

def normalize_label(x):
    if (x < 0):
        return 0.5 - x * (-0.5)
    else:
        return x * 0.5 + 0.5

def main():
    changeSpeed()
    joy = xbox.Joystick()
    last_trig = False
    last_x = 0
    data = ''
    start_time = time.time()
    angle = 180
    last_is_home = False
    while True:
        t = joy.rightTrigger()
        x = joy.rightX()
        cur_trig = t > 0
        if (not(last_trig == cur_trig)):
            last_trig = cur_trig
            if (cur_trig == 0.0):
                send_data(tcpCliSock, 'stop    ')
            if (cur_trig > 0):
                send_data_angle(tcpCliSock, 'forward ', str(angle), x, start_time)
        elif (not(x == last_x)):
            last_x = x
            if (x > -0.03 and x < 0.03):
                if not(last_is_home):
                    start_time = send_data_angle(tcpCliSock, 'home', '180', x, start_time)
                last_is_home = True
            else:
                last_is_home = False
                if (x > 0.03):
                    angle = int(x * 45 + 180)
                if (x < -0.03):
                    angle = int(180 + x * 144)
                if (angle == 180):
                    continue
                str_angle = str(angle)
                data = 'turn=' + str_angle
                start_time = send_data_angle(tcpCliSock, data, str_angle, x, start_time)

def send_data(tcpCliSock, data):
    data = ajust_buffer(data)
    print data
    tcpCliSock.send(data)
    tcpCliSock.recv(64)

def ajust_buffer(string):
    while len(string) < 12:
        print string
        string += ' '
    return string

def send_data_angle(tcpCliSock, data, angle, label, start_time):
    exec_time = time.time() - start_time
    if (exec_time >= 0.1):
        data = ajust_buffer(data)
        tcpCliSock.send(data)
        print 'sent_data',data
        tcpCliSock.recv(64)
        label = normalize_label(label)
        label = "%.4f" % label
        str_label = str(label)
        print 'sent_label',label
        data = 'OK' + label
        data = ajust_buffer(data)
        tcpCliSock.send(data)
        tcpCliSock.recv(64)
        start_time = time.time()
    else:
        data = ajust_buffer(data)
        tcpCliSock.send(data)
        tcpCliSock.recv(64)
    return start_time

if __name__ == '__main__':
	main()
