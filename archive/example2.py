from pykinect import nui
import pykinect 
import cv2
import numpy

# DEPTH_WINSIZE = 320,240

def depth_handler_function(frame):
	video = numpy.empty((480,640,4), numpy.uint8)
	frame.image.copy_bits(video.ctypes.data)
	cv2.imshow('KINECT Video Stream', video)

kinect = nui.Runtime()
kinect.depth_frame_ready += depth_handler_function
kinect.depth_stream.open(nui.ImageStreamType.Depth,2,nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)

cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

while True:
	key = cv2.waitKey(1)
	if key == 33: break

kinect.close()
cv2.destroyAllWindow()
