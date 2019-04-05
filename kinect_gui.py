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
from kivy.uix.spinner import Spinner
import cv2
import xlwt 
import os
import datetime
import csv
import shutil
import seaborn as sns
import numpy as np 
import matplotlib.pyplot as plt
import csv
import pandas as pd 
import ctypes

t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
# Kinect = False
# IMU = False

class LoginScreen(Screen):

    def submit_name(self):
        self.physicianname = self.physicianname_text_input.text
        self.patientname = self.patientname_text_input.text
        self.save()
        self.physicianname = ''
        self.patientname = ''

    def save(self):
        # make patient name folder if does not exist 
        global patient
        patient = str(self.patientname).lower()
        path = "C:\Users\esese\Documents\\" + patient

        # within that folder, make date/time folder 
        if not os.path.isdir(path): 
            os.makedirs(path)
        os.makedirs(path + '\\' + t) 

        global Kinect
        Kinect = False
        global IMU
        IMU = False
    
class MainScreen(Screen):
	pass

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

        dest = "C:\Users\esese\Documents\\" + patient + '\\' + t 
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
        path = "C:\Users\esese\Documents\\" + patient
        # read in csv 
        data = []
        with open(path + '\\' + t + '\\kinect.csv') as csv_file: # will need to change this path
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

        sns.set()
        plt.plot(avdf['Time (s)'], avdf['Average'], 'k--')
        plt.scatter(df['Time (s)'], df[variable], color = color)
        plt.xlabel('Time (s)')
        plt.ylabel(variable + ' (deg)')
        plt.title(variable)
        plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
        plt.show()

    def imu_graph(self, variable): 
        global patient
        path = "C:\Users\esese\Documents\\" + patient
        # read in csv 
        data = []
        with open(path + '\\' + t + '\\imu.csv') as csv_file: # will need to change this path
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

        sns.set()
        plt.plot(avdf['Time (s)'], avdf['Average'], 'k--')
        plt.scatter(df['Time (s)'], df[variable], color = color)
        plt.xlabel('Time (s)')
        plt.ylabel(variable + ' (quaternions)')
        plt.title(variable)
        plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
        plt.show()

    def moving_average(self, data, fs): 
        N = fs/5 # frame rate divided by five - for kinect, 200ms
        return np.convolve(data, np.ones((N,))/N, mode='valid')

class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("Main.kv")


class MainApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
	MainApp().run()
