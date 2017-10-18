#!/usr/bin/python

from __future__ import print_function
import time
import RPi.GPIO as GPIO

from threading import Thread

# -----------------------
# Define sensor parameters
# -----------------------

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)


# -----------------------
# Define measurement functions
# -----------------------
def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure_average(sleep_time=0.1):
  # This function takes 3 measurements and
  # returns the average.
  sleep_time /= 3
  distance1=measure()
  time.sleep(sleep_time)
  distance2=measure()
  time.sleep(sleep_time)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  return distance / 3

def setup():
  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BCM)

  #print("Ultrasonic measurement setup:")
  #print("Speed of sound is",speedSound/100,"m/s at ",temperature,"deg")

  # Set pins as output and input
  GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
  GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER, False)

  # Allow module to settle
  time.sleep(0.5)


def run(sleep_time=1):
  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.
  try:
    while True:
      distance = measure_average() # takes ~0.2 seconds
    print("Distance : {0:5.1f}".format(distance))
    time.sleep(sleep_time)

  except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    GPIO.cleanup()


### Usage:
# - Create UltrasonicAsync instance
# - Call run() method
# - Read dist field when needed
# - When done, call stop() then join() methods to properly close the thread

class UltrasonicAsync(Thread):

  def __init__(self, sleep_time):
    Thread.__init__(self)
    print("Setup ultrasonic sensor...")
    self.sleep_time = sleep_time
    setup()
    self.dist = measure_average(self.sleep_time)
    self.stop_flag = False
    print("Setup done!")
    # Add config code here

  def obstacle_near():
    return self.dist < 100

  def stop(self):
    self.stop_flag = True

  def run(self):
    self.stop_flag = False
    while not stop_flag:
      self.dist = measure_average(self.sleep_time)
    GPIO.cleanup()
