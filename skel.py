import pykinect
from pykinect import nui
from pykinect.nui import JointId
# from pykinect.nui import NuiImageGetColorPixelCoordinatesFromDepthPixel 
# from pykinect import pykinect
# from pykinect.PyKinectV1 import *
# from pykinect import PyKinectRuntime
# from pykinect import PyKinect
# from pykinect import P
# from pykinect import * 
import time 
import cv2
import numpy as np
import ctypes


L = 640
H = 480
# MapSkeletonPointToColorPoint
# sensor = ctypes.POINTER(IKinectSensor)()

## kinect video streaming ##
def video_handler_function(frame):
	# frame = np.array(frame)
	video = np.empty((480,640,4), np.uint8)
	coords = track_skel()
	if coords != None:
		# coords = kinect.body_joint_to_color_space(coords)
		# coords = convert_coords(coords.x, coords.y) 
		coords = convert_coords(coords)
		# coords = (coords.x, coords.y)
		print(coords)
	frame.image.copy_bits(video.ctypes.data)
	# if coords != None: 
		# cv2.circle(video,(int(coords[0]),int(coords[1])), 12, (0,0,255), 1)
	cv2.imshow('KINECT Video Stream', video)

def track_skel(): 
	frame = kinect.skeleton_engine.get_next_frame()                            
	for skeleton in frame.SkeletonData:                                                     # We check frame's skeleton data
		if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:                    # Check if skeleton is set as TRACKED
			coordinates = skeleton.SkeletonPositions                                            # skeleton.position returns our coordinates
			# print "Head: " + str(coordinates[JointId.Head])
			return coordinates[JointId.Head]

def convert_coords(coords): 
	#input in meters 
	#need output in pixels 
	# return (x*1000*96/25.4, y*1000*96/25.4)
	return nui.SkeletonEngine.skeleton_to_depth_image(coords) 

kinect = nui.Runtime()
# sensor = PyKinectRuntime() 
kinect.video_frame_ready += video_handler_function
kinect.skeleton_engine.enabled = True   
kinect.video_stream.open(nui.ImageStreamType.Video,2,nui.ImageResolution.Resolution640x480, nui.ImageType.Color)

cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

while True:

	key = cv2.waitKey(1)
	if key == 33: break

time.sleep(0.1)  

kinect.close()
cv2.destroyAllWindow()  