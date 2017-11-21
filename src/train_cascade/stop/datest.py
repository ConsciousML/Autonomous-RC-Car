from test import *
import glob

count = 0
time = 0
for i in range(0, 3000):
	files = glob.glob('left_dataset/{}_*.jpg'.format(i))
	if len(files) != 0:
		time += detect_stop_from_file(files[0], timer=True)
		count += 1

print("Average time taken: {:.6f}".format(time / count))