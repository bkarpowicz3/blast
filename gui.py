import tkinter as tk
import time
from glob import glob
import datetime

global task_selections
task_selections = {}

global current_patient
current_patient = None

global data_dir 
data_dir= 'Patient_Metrics'

## TODO: os.mkdir(path)

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

    #set up filesystem 
    #if patient is still None, then raise a warning window 
    session = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

    if len(task_selections) <= 0: 
        win = tk.Toplevel() 
        win.geometry('400x100')
        win.wm_title("No Task Selection")

        l = tk.Label(win, text = "Please select at least one task.")
        l.grid(row = 0, column = 0)
        b = tk.Button(win, text = 'OK', 
                command = win.destroy)
        b.grid(row = 1, column = 0)

        win.wait_window(window = win)
        return
    else: 
        new_dict = {}
        for t in task_selections.keys(): 
            val = task_selections[t]
            t = t.lower().replace(' ', '')
            new_dict[t] = val
        globals().update(task_selections = new_dict)
        # print(task_selections)

    # return 

    if current_patient == None: 
        win = tk.Toplevel()
        win.geometry('400x100')
        win.wm_title("No Patient Selected")

        l = tk.Label(win, text = "Please enter a new patient or select an existing patient!")
        l.grid(row = 0, column = 0)
        b = tk.Button(win, text = "OK",
                command = win.destroy)
        b.grid(row = 1, column = 0)

        win.wait_window(window = win)
        return
    else: 
        #if patient is selected, then check to see if there is already a directory for them 
        #if not, then make one 
        patient_dirs = glob(data_dir + "/*/")
        print(patient_dirs)
        if data_dir + '/' + current_patient + '/' not in patient_dirs: 
            os.makedirs(data_dir + '/' + current_patient)
        savepath = data_dir + '/' + current_patient + '/' + session
        os.makedirs(savepath)

    #within the directory, make one for the new date/time for session 

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

    for task in task_selections.keys(): 
        for i in range(0, int(task_selections[task])): 
            #loops through, save videos
            # pass 

            # Define the codec and create VideoWriter object to save the video
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer_original = cv2.VideoWriter(savepath + '/raw_output_' + task + '_' + str(i) + '.avi', fourcc, 20.0, (int(w), int(h)))

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

    videos = glob(savepath + '/*.avi')

    for v in videos: 
        filename = v.split('.')
        video_writer_openpose = cv2.VideoWriter(savepath + '/' + filename[0] + 'openpose' + '.avi', fourcc, 20.0, (int(w), int(h)))

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
        with open(savepath + filename[0] + '.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(point_store)

def save_selections(window, checkvars, checkboxes, inputs): 
    for i in range(0, len(checkboxes)):  
        if checkvars[i].get(): 
            task_selections[checkboxes[i].cget('text')] = inputs[i].get()
    # print(task_selections)
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

def select_old_patient(window, menu): 
    set_current_patient(menu.get())
    window.destroy()
    # print(current_patient)

def oldpatient(): 
    oldpatients = []
    f = open(data_dir + '/patients.txt', 'r')
    for patient in f.readlines():
        patient = patient.strip('\n')
        if patient != '': 
            oldpatients.append(patient)
    # print(oldpatients)
    f.close()
    
    win = tk.Toplevel()
    win.geometry('200x100')

    l = tk.Label(win, text = "Select Patient: ")
    l.grid(row = 0, column = 0)

    var = tk.StringVar(win)
    var.set(oldpatients[0]) #default
    menu = tk.OptionMenu(win, var, *oldpatients)
    menu.grid(row = 0, column = 1)

    b = tk.Button(win, 
                text = "Submit", 
                fg = 'blue', 
                command = lambda: select_old_patient(win, var))
    b.grid(row = 1, column = 1)

    b2 = tk.Button(win, 
                text = "Cancel", 
                fg = "red", 
                command = win.destroy)
    b2.grid(row = 1, column = 0)

def submit_new_patient(window, e): 
    set_current_patient(e.get())
    f = open(data_dir + '/patients.txt', 'a') 
    # print(current_patient)
    f.write(current_patient + '\n')
    f.close()
    window.destroy()

def newpatient():
    win = tk.Toplevel()
    win.geometry('250x100')

    l = tk.Label(win, text="New Patient Name: ")
    l.grid(row = 0, column = 0)
    e = tk.Entry(win, width = 10)
    e.grid(row = 0, column = 1)

    # win.grid_rowconfigure(1, minsize=75)

    b = tk.Button(win,
                text = "Submit",
                fg = 'blue',
                command = lambda: submit_new_patient(win, e))
    b.grid(row = 2, column = 1)

    b2 = tk.Button(win, 
                text = "Cancel", 
                fg = 'red',
                command = win.destroy)
    b2.grid(row = 2, column = 0)

def set_current_patient(patientname): 
    patientname = patientname.lower().replace(' ', '')
    # print(patientname)
    globals().update(current_patient = patientname)

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
                   command = quit)
quit_button.grid(row = 4, column = 1, sticky = tk.NSEW)

start_button = tk.Button(frame,
                   text="START", 
                   fg = 'blue',
                   # command = quit)
                   command=openpose_capture)
start_button.grid(row = 4, column = 2, sticky = tk.NSEW)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(3, weight=1)

root.mainloop()







