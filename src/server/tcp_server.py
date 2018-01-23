#/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import cv2
import numpy
import threading
from socket import *
from time import ctime          # Import necessary modules
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 12       # Size of the buffer
ADDR = (HOST, PORT)
FOLDER = "pictures/"

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server.
tcpSerSock.listen(5)     # The parameter of listen() defines the number of connections permitted at one time. Once the
                         # connections are full, others will be rejected.

video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor.
video_dir.home_x_y()
car_dir.home()

cam = PiCamera()
cam.resolution = (640, 480)

cam.hflip = True
cam.vflip = True

time.sleep(2)

i = 530

class ImgThread(threading.Thread):
    def __init__(self, angle, speed, folder, cam):
        threading.Thread.__init__(self)
        self.angle = angle
        self.folder = folder
        self.cam = cam
        self.speed = speed

    def run(self):
        global i
        i += 1

        path = self.folder + str(i) + "_" + str(self.angle) + "_" + str(self.speed) + ".jpg"
        print path

        cam.capture(path, use_video_port=True)

while True:
    print 'Waiting for connection...'
    # Waiting for connection. Once receiving a connection, the function accept() returns a separate
    # client socket for the subsequent communication. By default, the function accept() is a blocking
    # one, which means it is suspended before the connection comes.
    tcpCliSock, addr = tcpSerSock.accept()
    tcpCliSock.setblocking(0)
    print '...connected from :', addr     # Print the IP address of the client connected with the server.
    angle = 125
    start_time = time.time()
    cam_state = False
    while True:
        data = ''
        try:
            exec_time = time.time() - start_time
            if (cam_state == True and exec_time >= 0.4):
                start_time = time.time()
                ImgThread(angle, spd, FOLDER, cam).run()
            data = tcpCliSock.recv(BUFSIZ).strip()    # Receive data sent from the client
            tcpCliSock.send('OK')
            #print 'command receved'
            #if (len(data) > 2 and data[0] == 'O' and data[1] == 'K'):

            # Analyze the command received and control the car accordingly.
            if not data:
                break
            if data == 'Start':
                cam_state = True
            elif data == 'Stop':
                cam_state = False
            elif data == ctrl_cmd[0]:
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
                angle = 125
                car_dir.home()
            elif data == ctrl_cmd[4]:
                print 'recv stop cmd'
                motor.ctrl(0)
            elif data == ctrl_cmd[5]:
                print 'read cpu temp...'
                temp = cpu_temp.read()
                tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
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
        except:
            continue

tcpSerSock.close()
