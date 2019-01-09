import pykinect
from pykinect import nui
from pykinect.nui import JointId
import time 
import cv2
import numpy as np
import math
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

# kinect video streaming
def video_handler_function(frame):
	video = np.empty((480,640,4), np.uint8)
	frame.image.copy_bits(video.ctypes.data)	
	coords = track_skel()
	if coords != None:
		# print("Tracking...")
		converted_coords = [convert_coords(c.x, c.y, c.z) for c in coords]
		try:
			for center in converted_coords:
				cv2.circle(video, (int(center.x), int(center.y)), 12, (0,0,255), 2)
			plot_lines(converted_coords, video)
		except: 
			pass
		compute_metrics(converted_coords, video)
	else:
		cv2.putText(video, "SUBJECT IS TOO CLOSE TO DEVICE", (40,50), cv2.FONT_HERSHEY_SIMPLEX, float(1), (0,0,255), 2)
	cv2.imshow('KINECT Video Stream', video)

# obtains skeletal coordinates in Kinect space 
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

# uses dll to convert coordinates to color image space 
def convert_coords(x, y, z): 
	color = conv.ConvertPoints(x, y, z)
	return color

# plots lines between joints 
def plot_lines(converted_coords, video): 
	head = converted_coords[0]
	neck = converted_coords[1]
	shoulderL = converted_coords[2]
	elbowL = converted_coords[3]
	wristL = converted_coords[4]
	handL = converted_coords[5]
	shoulderR = converted_coords[6]
	elbowR = converted_coords[7]
	wristR = converted_coords[8]
	handR = converted_coords[9]
	hip = converted_coords[10]
	spine = converted_coords[11]
	cv2.line(video, (int(head.x), int(head.y)), (int(neck.x), int(neck.y)), (0,0,255), 2)
	cv2.line(video, (int(neck.x), int(neck.y)), (int(spine.x), int(spine.y)), (0,0,255), 2)
	cv2.line(video, (int(hip.x), int(hip.y)), (int(spine.x), int(spine.y)), (0,0,255), 2)
	cv2.line(video, (int(neck.x), int(neck.y)), (int(shoulderL.x), int(shoulderL.y)), (0,0,255), 2)
	cv2.line(video, (int(neck.x), int(neck.y)), (int(shoulderR.x), int(shoulderR.y)), (0,0,255), 2)
	cv2.line(video, (int(shoulderL.x), int(shoulderL.y)), (int(elbowL.x), int(elbowL.y)), (0,0,255), 2)
	cv2.line(video, (int(elbowL.x), int(elbowL.y)), (int(wristL.x), int(wristL.y)), (0,0,255), 2)
	cv2.line(video, (int(handL.x), int(handL.y)), (int(wristL.x), int(wristL.y)), (0,0,255), 2)
	cv2.line(video, (int(elbowR.x), int(elbowR.y)), (int(shoulderR.x), int(shoulderR.y)), (0,0,255), 2)
	cv2.line(video, (int(elbowR.x), int(elbowR.y)), (int(wristR.x), int(wristR.y)), (0,0,255), 2)
	cv2.line(video, (int(wristR.x), int(wristR.y)), (int(handR.x), int(handR.y)), (0,0,255), 2)

def compute_metrics(converted_coords, video): 
	shoulderL = converted_coords[2]
	elbowL = converted_coords[3]
	wristL = converted_coords[4]
	shoulderR = converted_coords[6]
	elbowR = converted_coords[7]
	wristR = converted_coords[8]

	#shoulder angle 
	y = abs(shoulderL.y - shoulderR.y);  
	x = abs(shoulderL.x - shoulderR.x); 
	shoulder_angle = round(math.degrees(math.atan(y/x)), 3);
	cv2.putText(video, "Shoulder Angle: " + str(shoulder_angle), (40,400), cv2.FONT_HERSHEY_SIMPLEX, float(0.5), (0,0,255), 2)

	#left elbow angle calculation
	elbow_angle(elbowL, wristL, shoulderL, "Left", 420, video)
	#right elbow angle calculation
	elbow_angle(elbowR, wristR, shoulderR, "Right", 440, video)

def elbow_angle(elbowL, wristL, shoulderL, LoR, posv, video): 
	#distance between the elbow and wrist
	elb_wristLy = abs(elbowL.y - wristL.y);
	elb_wristLx = abs(elbowL.x - wristL.x);
	elb_wristLhyp = np.sqrt(elb_wristLy**2 + elb_wristLx**2);
	#distance between elbow and shoulder
	elb_shoulderLy = abs(elbowL.y - shoulderL.y);
	elb_shoulderLx = abs(elbowL.x - shoulderL.x);
	elb_shoulderLhyp = np.sqrt(elb_shoulderLy**2 + elb_shoulderLx**2);
	#distance between wrist and shoulder
	wrist_shoulderLy = abs(wristL.y - shoulderL.y);
	wrist_shoulderLx = abs(wristL.x - shoulderL.x);
	wrist_shoulderLhyp = np.sqrt(wrist_shoulderLy**2 + wrist_shoulderLx**2);
	#find angle opposite elb-shoulder length
	C = math.degrees(math.acos((-elb_shoulderLhyp**2 + wrist_shoulderLhyp**2 + elb_wristLhyp**2)/(2*elb_wristLhyp*wrist_shoulderLhyp)));
	#find angle alpha
	alpha = 90-C;
	#find distance a-x and then elbow angle 
	a_x = elb_wristLhyp*math.cos(np.deg2rad(C));
	xdist = wrist_shoulderLhyp - a_x;
	beta = math.degrees(math.asin(xdist/elb_shoulderLhyp));
	elbow_angleL = alpha+beta;
	elbow_angleL = round(elbow_angleL, 3);
	cv2.putText(video, LoR + " Elbow Angle: " + str(elbow_angleL), (40,posv), cv2.FONT_HERSHEY_SIMPLEX, float(0.5), (0,0,255), 2)


#runtime code  
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