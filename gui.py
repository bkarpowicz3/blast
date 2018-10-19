import tkinter as tk

task_selections = {}
global task_selections

current_patient = None
global current_patient

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

def save_selections(window, checkvars, checkboxes, inputs): 
    for i in range(0, len(checkboxes)):  
        if checkvars[i].get(): 
            task_selections[checkboxes[i].cget('text')] = inputs[i].get()
    print(task_selections)
    window.destroy()

def select_tasks(): 
    win = tk.Toplevel()
    win.geometry('300x300')
    win.wm_title("Select Tasks")
    win.grid_columnconfigure(1, minsize=75)

    var1 = tk.IntVar()
    c1 = tk.Checkbutton(win, text="task 1", variable=var1)
    c1.grid(row = 0, sticky = tk.W)
    var2 = tk.IntVar()
    c2 = tk.Checkbutton(win, text="task 2", variable=var2)
    c2.grid(row = 1, sticky = tk.W)
    var3 = tk.IntVar() 
    c3 = tk.Checkbutton(win, text="task 3", variable=var3)
    c3.grid(row = 2, sticky = tk.W)

    e1 = tk.Entry(win, width = 10)
    e1.grid(row = 0, column = 2)
    e1.insert(0, "10")
    e2 = tk.Entry(win, width = 10)
    e2.grid(row = 1, column = 2)
    e2.insert(0, "10")
    e3 = tk.Entry(win, width = 10)
    e3.grid(row = 2, column = 2)
    e3.insert(0, "10")

    checkvars = [var1, var2, var3]
    checkboxes = [c1, c2, c3]
    inputs = [e1, e2, e3]

    close_button = tk.Button(win, 
                        text = 'Cancel',
                        fg = 'red',
                        command = win.destroy)
    close_button.grid(row = 10, column = 0)

    finish_button = tk.Button(win,
                        text = 'Done',
                        fg = 'blue', 
                        command = lambda: save_selections(win, checkvars, checkboxes, inputs))
    finish_button.grid(row = 10, column = 2)

def oldpatient(): 
    pass

def newpatient():
    pass

root = tk.Tk()
root.geometry('500x500') 
frame = tk.Frame(root)
frame.pack()

select_button = tk.Button(frame, 
                    text = "Select Tasks",
                    # fg = 'blue',
                    command = select_tasks)
select_button.grid(row = 1, column = 1, columnspan = 2, sticky = tk.NSEW)

oldpatient_button = tk.Button(frame, 
                        text="Select Existing Patient", 
                        command = oldpatient)
oldpatient_button.grid(row = 2, column = 1, columnspan = 2, sticky = tk.NSEW)

newpatient_button = tk.Button(frame,
                        text = "Input New Patient", 
                        command = newpatient)
newpatient_button.grid(row = 3, column = 1, columnspan = 2, sticky = tk.NSEW)

quit_button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
quit_button.grid(row = 4, column = 1, sticky = tk.NSEW)

start_button = tk.Button(frame,
                   text="START", 
                   fg = 'blue',
                   command = quit)
                   #command=openpose_capture)
start_button.grid(row = 4, column = 2, sticky = tk.NSEW)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()







