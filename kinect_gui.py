from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
import kivy.uix.screenmanager
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
import cv2
import xlwt 
import os
# from xlwt import Workbook
import datetime
import csv
import shutil
from kivy.uix.spinner import Spinner
import seaborn as sns
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import pandas as pd 
import ctypes
import glob
from Tkinter import *

global t
t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
global Kinect
Kinect = False
global IMU
IMU = False 
global valid_graphs 

with open('destination.txt') as file:
    default_path = file.readline()

class MainScreen(Screen):
    pass

class LoginScreen(Screen):

    def submit_name(self):

        self.physicianname = self.physicianname_text_input.text
        self.patientname = self.patientname_text_input.text
        global patient
        global physicianname
        physicianname = str(self.physicianname).lower()
        patient = str(self.patientname).lower()
        t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
        

    def check_login(self):
        if self.ids["Physician_Name"].text != "" and self.ids["Patient_Name"].text != "":
            self.manager.current = 'savefile'
        else:
            self.manager.current = 'login'


class LoadDataScreen(Screen):
    pass

class OlddataScreen(Screen):

    def submit_name(self):

        self.newpatientname = self.newpatientname_text_input.text
        self.dateformat = self.dateformat_text_input.text
        global patient
        patient = str(self.newpatientname).lower()
        

    def check_loaddata(self):
        global patient 
        global Kinect
        global IMU
        global valid_graphs
        valid_graphs = []
        nameGood = False
        dateGood = False

        if self.ids["Patient_Name"].text != "" and self.ids["Date"].text != "":
            # self.manager.current = 'Dataanalysis'
            nameGood = True

        if len(self.ids["Patient_Name"].text) > 0: 
            # self.manager.current = 'Dataanalysis' 
            pass
        else: 
            ctypes.windll.user32.MessageBoxW(0, u"Enter Patient Name!", u"Error", 16) 
            # self.manager.current = 'olddata'

        date = self.ids["Date"].text    

        furtherCheck = False
        if self.ids["Date"].text.isdigit() and len(date) == 8: 
            m = date[0:2]
            d = date[2:4]
            y = date[4:8]
            furtherCheck = True
        else: 
            ctypes.windll.user32.MessageBoxW(0, u"Date must be numbers (mmddyyyy)!", u"Error", 16)
            # self.manager.current = 'olddata'

        if furtherCheck: 
            if int(m) >= 1 and int(m) <= 12 and int(d) >= 1 and int(d) <= 31 and int(y) >= 2018 and int(y) <= 3000: 
                # self.manager.current = 'Dataanalysis'
                dateGood = True
            else: 
                ctypes.windll.user32.MessageBoxW(0, u"Enter Valid Date.", u"Error", 16) 
                # self.manager.current = 'olddata'
        
        if nameGood and dateGood: 
            global selected_t 
            global t
            patient = self.ids["Patient_Name"].text.lower()
            t = y + "-" + m + '-' + d
            possible_times = glob.glob(default_path + '/' + patient + '/*/')
            if len(possible_times) >= 1:
                times = []
                for pt in possible_times: 
                    pt = pt.split('\\')
                    pt = pt[len(pt)-2]
                    pt = pt.split('-')
                    times.append(pt[len(pt)-1])
                if len(times) > 1: 
                    root = Tk()
                    root.title("Drop-down boxes for option selections.")
                    var = StringVar(root)
                    var.set("Select a Time and Close")

                    def grab_and_assign(event):
                        global selected_t
                        chosen_option = var.get()
                        label_chosen_variable= Label(root, text=chosen_option)
                        label_chosen_variable.grid(row=1, column=2)
                        selected_t = chosen_option

                    drop_menu = OptionMenu(root, var, *tuple(times), command=grab_and_assign)
                    drop_menu.grid(row=0, column=0)

                    label_left=Label(root, text="chosen variable= ")
                    label_left.grid(row=1, column=0)

                    root.mainloop()

                    t = t + '-' + selected_t
                else: 
                    t = t + '-' + times[0]

                files_available = glob.glob(default_path + '\\' + patient + '\\' + t + '\\*')
                if default_path + '\\' + patient + '\\' + t + '\\' + 'kinect.csv' in files_available: 
                    Kinect = True
                    valid_graphs.append('Left Elbow Angles')
                    valid_graphs.append('Right Elbow Angles')
                    valid_graphs.append('Shoulder Angles')
                if default_path + '\\' + patient + '\\' + t + '\\' + 'imu.csv' in files_available: 
                    IMU = True
                    valid_graphs.append('QX')
                    valid_graphs.append('QY')
                    valid_graphs.append('QZ')
                    valid_graphs.append('Q0')
                # print(t)

                # print(valid_graphs)

                self.manager.current = 'Dataanalysis'
            else: 
                ctypes.windll.user32.MessageBoxW(0, u"No sessions exist for this date.", u"Error", 16) 

class SaveFileScreen(Screen):
    labeltext = StringProperty(default_path)

    def save(self):
        global t 
        self.physicianname = ''
        self.patientname = ''
        t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
        patientpath = default_path + '\\' + patient
        if not os.path.isdir(patientpath): 
            os.makedirs(patientpath)
        os.makedirs(patientpath + '\\' + t) 


class SaveDialog(Screen):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def open(self,path,selection):
        with open('destination.txt', 'w') as f: 
            f.write(path)
            f.close()
        global default_path
        default_path = path
        self.save
        ctypes.windll.user32.MessageBoxW(0, u"The file is now saved in " + (default_path), u"Message", 16)
 

class ExerciseScreen(Screen):
    pass

class ListScreen(Screen): 

    def start_kinect(self):
        global Kinect
        os.system('python skel.py')
        Kinect = True
        
    def start_imu(self):
        global IMU
        os.system('python wearable_data.py')
        IMU = True

    def start_parallel(self):
        global Kinect
        global IMU
        os.system('python run_parallel.py')  
        Kinect = True
        IMU = True  

    def collect_data(self):
        global patient
        global valid_graphs
        global Kinect
        global IMU
        global t

        dest = default_path + '\\' + patient + '\\' + t 
        if Kinect:
            source1 = "C:\Users\esese\Documents\\blast-master\\kinect.csv"
            source3 = "C:\Users\esese\Documents\\blast-master\\kinect.avi"
            shutil.move(source1, dest)
            shutil.move(source3, dest)

        if IMU: 
            source2 = "C:\Users\esese\Documents\\blast-master\\imu.csv"
            shutil.move(source2, dest)

        valid_graphs = []
        if Kinect: 
            valid_graphs.append('Shoulder Angles')
            valid_graphs.append('Left Elbow Angles')
            valid_graphs.append('Right Elbow Angles')

        if IMU: 
            valid_graphs.append('Q0')
            valid_graphs.append('QX')
            valid_graphs.append('QY')
            valid_graphs.append('QZ')
        
class DropdownScreen(Screen):

    def spinner_clicked(self, value):
        global valid_graphs
        # print(valid_graphs)

        kinect_graphs = ['Shoulder Angles', 'Left Elbow Angles', 'Right Elbow Angles']
        imu_graphs = ['Q0', 'QX', 'QY', 'QZ']

        if value not in valid_graphs: 
            ctypes.windll.user32.MessageBoxW(0, u"This data was not collected for this session.", u"Error", 16)
        else: 
            if value in kinect_graphs: 
                self.kinect_graph(value)
            if value in imu_graphs: 
                self.imu_graph(value)

    def kinect_graph(self, variable): 
        global patient
        global t
        data = []
        with open(default_path + '\\' + patient + '\\' + t + '\\kinect.csv') as csv_file: 
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                data.append(row)
            data = np.array(data)

        if variable == 'Shoulder Angles':
            toplot = data[:, 0]
            color = 'blue'
        elif variable == 'Left Elbow Angles': 
            toplot = data[:, 1]
            color = 'red'
        elif variable == 'Right Elbow Angles':  
            toplot = data[:, 2]
            color = 'green'

        df = pd.DataFrame(toplot)
        df = df.astype('float')
        df.columns = [variable]

        fs = 30 #frames per second 
        time = np.linspace(0, len(toplot)/float(fs), len(toplot))

        df['Time (s)'] = time

        mov_av = self.moving_average(np.array(df[variable])[1:len(toplot)], fs)  
        time_resampled = np.linspace(0, len(toplot)/float(fs), len(mov_av))
        avdf = pd.DataFrame(mov_av)
        avdf.columns = ['Average']
        avdf['Time (s)'] = time_resampled

        def onpick(event):
            ind = event.ind[0] #index of selected dot (the earliest one)
            pos_x = event.mouseevent.xdata
            pos_y = event.mouseevent.ydata 
            get_frame(pos_x, pos_y)

        def get_frame(x, y):
            which_frame = x*fs
            vidcap = cv2.VideoCapture(default_path + '\\' + patient + '\\' + t + '\\kinect.avi')
            success,image = vidcap.read()
            # print('read frame')
            count = 0
            success = True
            while success: 
                if count == np.floor(which_frame): 
                    # print('writes frames')
                    cv2.imwrite("frame%d.jpg" % count, image)
                    # print('writes image')
                    img = mpimg.imread('frame%d.jpg' % count)
                    # print('reads img')
                    fig = plt.figure()
                    ax = plt.subplot()
                    imgplot = ax.imshow(img)
                    ax.axis('off')
                    plt.show()
                    print('shows')
                    break
                else: 
                    success,image = vidcap.read()
                    count += 1
            # print(count)

        # print(df.shape)
        sns.set()
        fig = plt.figure()
        ax = plt.subplot()
        ax.plot(avdf['Time (s)'], avdf['Average'], 'k--')
        ax.scatter(df['Time (s)'], df[variable], color = color, picker = True)
        ax.set_ylim(0, 180)
        plt.xlabel('Time (s)')
        plt.ylabel(variable + ' (deg)')
        plt.title(variable)
        plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
        
        fig.canvas.mpl_connect('pick_event', onpick)

        plt.show()

    def imu_graph(self, variable): 
        global patient
        global Kinect
        global t

        data = []
        with open(default_path + '\\' + patient + '\\' + t + '\\imu.csv') as csv_file: 
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                data.append(row)
            data = np.array(data)

        if variable == 'Q0':
            toplot = data[:, 0]
            color = 'darkviolet'
        elif variable == 'QX': 
            toplot = data[:, 1]
            color = 'darkorange'
        elif variable == 'QY':  
            toplot = data[:, 2]
            color = 'hotpink'
        else: 
            toplot = data[:,3]
            color = 'gray'

        df = pd.DataFrame(toplot)
        df = df.astype('float')
        df.columns = [variable]

        fs = 30 #frames per second 
        time = np.arange(0, len(toplot)/float(fs), 1.0/fs)

        df['Time (s)'] = time

        mov_av = self.moving_average(np.array(df[variable])[1:len(toplot)], fs)  
        time_resampled = np.linspace(0, len(toplot)/float(fs), len(mov_av))
        avdf = pd.DataFrame(mov_av)
        avdf.columns = ['Average']
        avdf['Time (s)'] = time_resampled

        def onpick(event):
            ind = event.ind[0] #index of selected dot (the earliest one)
            pos_x = event.mouseevent.xdata
            pos_y = event.mouseevent.ydata 
            get_frame(pos_x, pos_y)

        def get_frame(x, y):
            which_frame = x*fs
            vidcap = cv2.VideoCapture(default_path + '\\' + patient + '\\' + t + '\\kinect.avi')
            success,image = vidcap.read()
            # print('read frame')
            count = 0
            success = True
            while success: 
                if count == np.floor(which_frame): 
                    # print('writes frames')
                    cv2.imwrite("frame%d.jpg" % count, image)
                    # print('writes image')
                    img = mpimg.imread('frame%d.jpg' % count)
                    # print('reads img')
                    fig = plt.figure()
                    ax = plt.subplot()
                    imgplot = ax.imshow(img)
                    ax.axis('off')
                    plt.show()
                    # print('shows')
                    break
                else: 
                    success,image = vidcap.read()
                    count += 1

        sns.set()
        fig = plt.figure()
        ax = plt.subplot()
        ax.plot(avdf['Time (s)'], avdf['Average'], 'k--')
        ax.scatter(df['Time (s)'], df[variable], color = color, picker = True)
        plt.xlabel('Time (s)')
        plt.ylabel(variable + ' (quaternions)')
        # ax.set_ylim(0, 180)
        plt.title(variable)
        plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
        
        if Kinect:
            fig.canvas.mpl_connect('pick_event', onpick)

        plt.show()

    def moving_average(self, data, fs): 
        N = fs/3 # frame rate divided by five - for kinect, 200ms
        return np.convolve(data, np.ones((N,))/N, mode='valid')


class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("Main.kv")


class MainApp(App):
    def build(self):
        return presentation
        return SaveDialog

if __name__ == '__main__':
    MainApp().run()