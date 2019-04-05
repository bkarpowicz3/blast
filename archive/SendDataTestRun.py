import serial
import cv2
import numpy as np

data = serial.Serial('COM3', 115200)

store = []

while True:
	d = data.readline()
	# will need to parse d into array of [x y z w] values 
	store.append(d)

    key = cv2.waitKey(32)
	if key == 32: break


a = np.asarray(store)
np.savetxt("imu.csv", a, delimiter=",")
