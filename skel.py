import pykinect
from pykinect import nui
from pykinect.nui import JointId
import time 
import cv2
import numpy as np
import ctypes
import sys
import clr

#add custom Kinect dll to workspace 
sys.path.append(r"C:\Users\Michael\source\repos\KinectConverter\KinectConverter\bin\Debug\netstandard2.0")
clr.AddReference(r"KinectConverter")

#object from dll
from KinectConverter import Converter 
conv = Converter() 

#color video dimensions
L = 640
H = 480

## kinect video streaming ##
def video_handler_function(frame):
	video = np.empty((480,640,4), np.uint8)
	frame.image.copy_bits(video.ctypes.data)	
	coords = track_skel()
	if coords != None:
		converted_coords = [convert_coords(c.x, c.y, c.z) for c in coords]
		for center in converted_coords:
			cv2.circle(video, (int(center.x), int(center.y)), 12, (0,0,255), 2)
	cv2.imshow('KINECT Video Stream', video)

	##TODO: fix issue where if too close code breaks - add try/catch and print warning 

def track_skel(): 
	joints = [JointId.Head, 
			JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft,
            JointId.ShoulderRight, 
            JointId.ElbowRight, 
            JointId.WristRight, 
            JointId.HandRight,
            JointId.HipCenter, 
         	JointId.Spine]
	frame = kinect.skeleton_engine.get_next_frame()                            
	for skeleton in frame.SkeletonData:                                                     
		if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:                    
			coordinates = skeleton.SkeletonPositions                                            
			return [coordinates[j] for j in joints]

def convert_coords(x, y, z): 
	color = conv.ConvertPoints(x, y, z)
	return color

kinect = nui.Runtime()
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