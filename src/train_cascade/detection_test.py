
import cv2

import os
import sys
import time
import glob


from stop.test import detect_stop
from obligation.test import detect_obligation


def detect_from_file(f, fname, show=False, timer=False, shape=(320, 240)):
  img = cv2.imread(fname)
  img = cv2.resize(img, shape)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  diff = 0

  if timer:
    start = time.time()
  stop_detected = f(img, gray, show=show, fname=fname)
  if timer:
    stop = time.time()
    diff = stop - start
    #print("{:.6f}s".format(diff))
  return diff, stop_detected

def positive_negative(f=detect_stop, dir='stop'):
  pos_dir = os.path.join(dir, 'positive')
  neg_dir = os.path.join(dir, 'negative')
  pos_files = os.listdir(pos_dir)
  neg_files = os.listdir(neg_dir)
  n_pos = len(pos_files)
  n_neg = len(neg_files)
  n_tot = n_pos + n_neg

  # false/true positive/negative
  tp = 0
  fp = 0
  tn = 0
  fn = 0

  time_tot = 0

  for pos in pos_files:
    fname = os.path.join(pos_dir, pos)
    time, stop_detected = detect_from_file(f, fname, timer=True)
    if stop_detected:
      tp += 1
    else:
      fn += 1
    time_tot += time

  for neg in neg_files:
    fname = os.path.join(neg_dir, neg)
    time, stop_detected = detect_from_file(f, fname, timer=True)
    if stop_detected:
      fp += 1
    else:
      tn += 1
    time_tot += time


  if n_pos == 0:
    n_pos = 1e50
  if n_neg == 0:
    n_neg = 1e50

  print('\nResults for function {}:\n'.format(f.__name__))
  print('Positive exemples: {}'.format(len(pos_files)))
  print('Negative exemples: {}\n'.format(len(neg_files)))
  print('- True positives: {} (should be as close as 1.0 as possible)'.format(tp / n_pos))
  print('- True negatives: {}'.format(tn / n_neg))
  print('- False positives: {} (should be 0)'.format(fp / n_neg))
  print('- False negatives: {}\n'.format(fn / n_pos))
  print('Average time taken: {}'.format(time_tot / n_tot))


def bench_time(f, data_dir):
  count = 0
  time_tot = 0
  for i in range(1000, 1500):
    files = glob.glob('{}/{}_*.jpg'.format(data_dir, i))
    if len(files) != 0:
      time, _ = detect_from_file(f, files[0], timer=True)
      time_tot += time
      count += 1

  print('Number of image tested: {}'.format(count))
  if count != 0:
    print("Average time taken: {:.6f}".format(time_tot / count))



if __name__ == '__main__':
  features = ['stop', 'obligation']

  # Configure test name for changing type of test
  test_name = 'stop'

  module_name = "{}.test".format(test_name)
  f_name = "detect_{}".format(test_name)
  f = getattr(sys.modules[module_name], f_name)
  positive_negative(f=f, dir=test_name)
  #bench_time(f=detect_stop, data_dir='stop/left_dataset')
