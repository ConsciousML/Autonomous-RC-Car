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

def normalize_label(old_val, old_min, old_max, new_min, new_max):
    old_val = float(old_val)
    new_val = (((old_val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
    return new_val

while True:
    t = joy.rightTrigger()
    val = normalize_label(t, 0.0, 1.0, 40, 100)
    print(val)
    """
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
    """
