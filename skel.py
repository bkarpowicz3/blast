import pykinect
from pykinect import nui
from pykinect.nui import JointId
import time 
import cv2
import numpy as np
import ctypes
import sys
import clr

#add Kinect dll to workspace 
# sys.path.append(r"C:\Program Files\Microsoft SDKs\Kinect\v1.8\Assemblies")
sys.path.append(r"C:\Users\Michael\source\repos\KinectConverter\KinectConverter\bin\Debug\netstandard2.0")
# clr.AddReference(r"Microsoft.Kinect")
clr.AddReference(r"KinectConverter")

##TODO: TRY WRITING YOUR OWN DLL SO THAT YOU CAN INSTANTIATE SENSOR OBJECT

#sensor object from dll
# from Microsoft.Kinect import Microsoft.Kinect
# from Microsoft.Kinect import KinectSensor
# from Microsoft.Kinect import KinectSensor, CoordinateMapper, DepthImageFormat, ColorImageFormat, SkeletonPoint
# sensor = KinectSensor #Microsoft.Kinect()
from KinectConverter import Converter 
conv = Converter() 

#color video dimensions
L = 640
H = 480

## kinect video streaming ##
def video_handler_function(frame):
	# frame = np.array(frame)
	video = np.empty((480,640,4), np.uint8)
	coords = track_skel()
	if coords != None:
		# coords = kinect.body_joint_to_color_space(coords)
		coords = convert_coords(coords.x, coords.y, coords.z) 
		# coords = convert_coords(coords)
		# coords = (coords.x, coords.y)
		print(coords.x, coords.y)
	frame.image.copy_bits(video.ctypes.data)
	if coords != None: 
		cv2.circle(video,(int(coords.x),int(coords.y)), 12, (0,0,255), 1)
	cv2.imshow('KINECT Video Stream', video)

def track_skel(): 
	frame = kinect.skeleton_engine.get_next_frame()                            
	for skeleton in frame.SkeletonData:                                                     # We check frame's skeleton data
		if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:                    # Check if skeleton is set as TRACKED
			coordinates = skeleton.SkeletonPositions                                            # skeleton.position returns our coordinates
			# print "Head: " + str(coordinates[JointId.Head])
			return coordinates[JointId.Head]

def convert_coords(x, y, z): 
	# cm = CoordinateMapper()
	# point = SkeletonPoint()
	# point.X = x
	# point.Y = y
	# point.Z = z
	# print(point)
	# color = CoordinateMapper.MapSkeletonPointToColorPoint(point, ColorImageFormat.RgbResolution640x480Fps30)
	# depth = CoordinateMapper.MapSkeletonPointToDepthPoint(point, DepthImageFormat.Resolution320x240Fps30)
	# depth = CoordinateMapper.MapSkeletonPointToDepthPoint(x, DepthImageFormat.Resolution320x240Fps30)
	# color = CoordinateMapper.MapDepthPointToColorPoint(DepthImageFormat.Resolution320x240Fps30, depth, ColorImageFormat.RgbResolution640x480Fps30);
	# color_y = CoordinateMapper.MapDepthPointToColorPoint(DepthImageFormat.Resolution320x240Fps30, depth_y, ColorImageFormat.RgbResolution640x480Fps30);
	color = conv.ConvertPoints(x, y, z)
	return color
	# return nui.SkeletonEngine.skeleton_to_depth_image(coords) 

kinect = nui.Runtime()
# kinect = PyKinectRuntime() 
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