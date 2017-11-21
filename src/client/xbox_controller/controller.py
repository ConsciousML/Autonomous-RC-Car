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
while True:
    t = joy.rightTrigger()
    x = joy.rightX()
    cur_trig = t > 0
    if (not(last_trig == cur_trig)):
        last_trig = cur_trig
        if (cur_trig == 0.0):
            print 'stop    '
        if (cur_trig > 0):
            print 'forward '
            print str(angle)
    elif (not(x == last_x)):
        last_x = x
        if (x < 0):
            display_x = 0.5 - x * -0.5
        else:
            display_x = x * 0.5 + 0.5

        if (x > -0.03 and x < 0.03):
            if not(last_is_home):
                print 'home    '
                print '180'
                print display_x
            last_is_home = True
        else:
            last_is_home = False
            if (x > 0.03):
                angle = int(x * 45 + 180)
            if (x < -0.03):
                angle = int(180 + x * 145)
            str_angle = str(angle)
            if (len(str_angle) == 1):
                data = 'turn=' + str(angle) + '  '
            if (len(str_angle) == 2):
                data = 'turn=' + str(angle) + ' '
            if (len(str_angle) == 3):
                data = 'turn=' + str(angle)
            print 'x: ',x
            print 'data: ',data,'\n'
            print display_x
