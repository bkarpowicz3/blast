import tkinter as tk

def openpose_capture(): 
    # From Python
    # It requires OpenCV installed for Python
    import sys
    import cv2
    import os
    from sys import platform
    import numpy as np
    from pynput import keyboard
    import csv 

    # Remember to add your installation path here
    dir_path = '/Users/briannakarpowicz/Documents/openpose/'
    sys.path.append('/Users/briannakarpowicz/Documents/openpose/build/python');

    # Parameters for OpenPose. Take a look at C++ OpenPose example for meaning of components. Ensure all below are filled
    try:
        # from openpose import *
        import openpose as op
    except:
        raise Exception('Error: OpenPose library could not be found.')

    params = dict()
    params["logging_level"] = 3
    params["output_resolution"] = "-1x-1"
    params["net_resolution"] = "-1x368"
    params["model_pose"] = "BODY_25"
    params["alpha_pose"] = 0.6
    params["scale_gap"] = 0.3
    params["scale_number"] = 1
    params["render_threshold"] = 0.05
    # If GPU version is built, and multiple GPUs are available, set the ID here
    params["num_gpu_start"] = 0
    params["disable_blending"] = False
    # Ensure you point to the correct path where models are located
    # params["default_model_folder"] = dir_path + "/../../../models/"
    params["default_model_folder"] = dir_path + "models/"
    # Construct OpenPose object allocates GPU memory
    openpose = op.OpenPose(params)
    # return openpose

# def openpose_capture(openpose): 
    print('opening webcam')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened(): 
        cap.open()

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT); 

    # Define the codec and create VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer_original = cv2.VideoWriter('raw_output.avi', fourcc, 20.0, (int(w), int(h)))
    video_writer_openpose = cv2.VideoWriter('openpose_output.avi', fourcc, 20.0, (int(w), int(h)))

    frame_store = []
    point_store = []

    recording = True
    while(recording):
        # Capture frame-by-frame    
        ret, frame = cap.read()
        # Display the frame
        cv2.imshow('frame',frame)
        frame_store.append(frame)
        video_writer_original.write(frame)
        k = cv2.waitKey(1)
        if k is 32: #press space to quit 
            break

    # When everything done, release the capture
    cap.release()
    video_writer_original.release()
    cv2.destroyAllWindows()
    # return frame_store, point_store, openpose

    counter = 0;
    for f in frame_store: 
        counter += 1
        progress = float(counter)/len(frame_store)
        if np.floor(progress % 10) == 0:
            print(str(progress * 100) + '% Complete' )
        # Our operations on the frame come here
        # This is the slow part
        keypoints, output_frame = openpose.forward(f, True)
        point_store.append(keypoints)
        video_writer_openpose.write(output_frame)

    video_writer_openpose.release()

    # Save points 
    with open('openpose_points.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(point_store)

root = tk.Tk()
root.geometry('500x500') 
frame = tk.Frame(root)
frame.pack()

# openpose = initialize_openpose()

button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.pack(padx = 5, pady = 10, side = tk.LEFT)
slogan = tk.Button(frame,
                   text="START",
                   command=openpose_capture)
slogan.pack(padx = 5, pady = 10, side = tk.LEFT)

root.mainloop()