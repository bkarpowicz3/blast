import pykinect
from pykinect import nui
import time 
import cv2
import numpy

## kinect video streaming ##
def video_handler_function(frame):
	video = numpy.empty((480,640,4), numpy.uint8)
	frame.image.copy_bits(video.ctypes.data)
	cv2.imshow('KINECT Video Stream', video)

kinect = nui.Runtime()
kinect.video_frame_ready += video_handler_function
kinect.video_stream.open(nui.ImageStreamType.Video,2,nui.ImageResolution.Resolution640x480, nui.ImageType.Color)

cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

while True:
	key = cv2.waitKey(1)
	if key == 27: break

kinect.close()
cv2.destroyAllWindow()

## Collect skeleton data ##
# kinect = nui.Runtime()
# kinect.skeleton_engine.enabled = True                                                    # We will only be detecting our skeleton

# while (True):
# 	frame = kinect.skeleton_engine.get_next_frame()                            # Getting only 1 frame
# 	for skeleton in frame.SkeletonData:                                                     # We check frame's skeleton data
# 		if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:                    # Check if skeleton is set as TRACKED
# 			coordinates = skeleton.SkeletonPositions                                            # skeleton.position returns our coordinates
# 			print "Head: " + str(coordinates[JointId.Head])

# time.sleep(0.1)    