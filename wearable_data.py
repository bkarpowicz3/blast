import serial
import cv2
import numpy as np
import re

data = serial.Serial('COM3', 115200)


store = []

while True:
	d = data.readline()
	# print d
	if 'qx' in d:
		video = np.empty((480,640,4), np.uint8)
		values = re.split(r'\t+', d)
		# print(values)
		values[3] = values[3].rstrip(' \t\n\r')

		cv2.putText(video, values[0], (40, 50), cv2.FONT_HERSHEY_SIMPLEX, float(1), (255,255,255), 2)
		cv2.putText(video, values[1], (40,100), cv2.FONT_HERSHEY_SIMPLEX, float(1), (255,255,255), 2)
		cv2.putText(video, values[2], (40,150), cv2.FONT_HERSHEY_SIMPLEX, float(1), (255,255,255), 2)
		cv2.putText(video, values[3], (40,200), cv2.FONT_HERSHEY_SIMPLEX, float(1), (255,255,255), 2)

		nums = []
		for v in values: 
			pieces = v.split()
			nums.append(float(pieces[2]))
		store.append(nums)

		cv2.imshow('IMU Data Stream', video)

	key = cv2.waitKey(32)
	if key == 32: 
		break

a = np.asarray(store)
np.savetxt("imu.csv", a, delimiter=",")