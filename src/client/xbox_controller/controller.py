import xbox
import math
import time

joy = xbox.Joystick()
last_trig = False
last_x = 0
data = ''
start_time = time.time()
angle = 180
last_is_home = False
last_start = 0
cam_state = 0
while True:
    t = joy.rightTrigger()
    x = joy.rightX()
    cur_trig = t > 0
    s = joy.Start()
    if (s != last_start):
        last_start = s
        if (s == 1):
            print cam_state
            if (cam_state == 0):
                cam_state = 1
                print 'Start'
            else:
                cam_state = 0
                print 'Stop'
    if (not(last_trig == cur_trig)):
        last_trig = cur_trig
        if (cur_trig == 0.0):
            print 'stop    '
        if (cur_trig > 0):
            print 'forward '
            print str(angle)
    elif (not(x == last_x)):
        last_x = x

        if (x > -0.03 and x < 0.03):
            if not(last_is_home):
                print 'home    '
                print '125'
            last_is_home = True
        else:
            last_is_home = False
            angle = ((x / 2) + 0.5) * 170 + 40
            str_angle = str(angle)
            print 'x: ',x
            print 'data: ',data,'\n'
            print str_angle
