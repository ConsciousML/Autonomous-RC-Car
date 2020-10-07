#!/usr/bin/env python
import PCA9685 as servo
import time                # Import necessary modules

"""

This function controls the car movement.

"""

last_dir = 0

def Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup(busnum=None):
    global leftPWM, rightPWM, homePWM, pwm
    leftPWM = 350
    homePWM = 450
    rightPWM = 550
    offset =0
    try:
        for line in open('config'):
            if line[0:8] == 'offset =':
                offset = int(line[9:-1])
    except:
      print 'config error'
    leftPWM += offset - 20
    homePWM += offset
    rightPWM += offset
    if busnum == None:
        pwm = servo.PWM()                  # Initialize the servo controller.
    else:
        pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.
    pwm.frequency = 60

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the
# car turn left.
# ==========================================================================================
def turn_left():
    global leftPWM
    global last_dir
    last_dir = -1
    pwm.write(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
    global rightPWM
    global last_dir
    last_dir = 1
    pwm.write(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
    global last_dir
    if (angle > 180):
        last_dir = 1
    else:
        last_dir = -1
    angle = Map(angle, 0, 255, leftPWM, rightPWM)
    pwm.write(0, 0, angle)

def home():
    global homePWM
    global last_dir
    off = 0
    if last_dir == 1:
        #right
        off = -30
    elif last_dir == -1:
        #left
        off = -5
    pwm.write(0, 0, homePWM + off)

def calibrate(x):
    pwm.write(0, 0, 450+x)

def test():
    while True:
        turn_left()
    time.sleep(1)
    home()
    time.sleep(1)
    turn_right()
    time.sleep(1)
    home()

if __name__ == '__main__':
    setup()
    home()

