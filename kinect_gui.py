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
import cv2
import xlwt 
import os
from xlwt import Workbook
import datetime
import csv
import shutil
from kivy.uix.spinner import Spinner
import seaborn as sns
import numpy as np 
import matplotlib.pyplot as plt
import csv
import pandas as pd 


wb = Workbook()
t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')

#Window.clearcolor = (0.3, 0.1, 0.1, 0)
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
        # save record of sesssion
        # sheet = wb.add_sheet('Sheet 1')
        # sheet.write(0,0,'Physician Name')
        # sheet.write(1,0,'Patient Name')
        # sheet.write(0,1, str(self.physicianname))
        # sheet.write(1,1, str(self.patientname))
        # sheet.write()
        # wb.save(path + '\\' + patient + '.xls')
        # add timestamps to this 
        # change to csv + make sure do not overwrite 
        # if not os.path.isdir(path + '\\' + patient): 
        #     os.makedirs(path + '\\' + patient + '.csv')
            # later add header row? 
            # with open(path + '\\' + patient +'.csv', 'wb') as csv_file: 
            #     writer = csv.writer(csv_file, delimiter = ',', quotechar = '|')
            #     #writer.writerow((str(self.physicianname) )
            #     writer.writerow(['Patient Name',str(self.patientname)])
            #     writer.writerow(['Physician Name',str(self.physicianname)])
            #     writer.writerow(['Date',(t)])
            # save kinect & arduino data inside date/time folder
            # with open(path + '\\' + t +'\\' + patient + t + '\\kinectdata.csv', 'wb') as csv_file: 
            #     writer = csv.writer(csv_file, delimiter = ',', quotechar = '|')
            # with open(path + '\\' + t +'\\' + patient + t + '\\imu.csv', 'wb') as csv_file: 
            #     writer = csv.writer(csv_file, delimiter = ',', quotechar = '|')
            # with open(path + '\\' + t +'\\' + patient + t + '\\ log.csv', 'wb') as csv_file: 
            #     writer = csv.writer(csv_file, delimiter = ',', quotechar = '|')
            #     writer.writerow(['Patient Name',str(self.patientname)])
            #     writer.writerow(['Physician Name',str(self.physicianname)])
            #     writer.writerow(['Date',(t)])
        # if os.path.exists(path + '\\' + patient): 
    # def newsave(self):
    #     patient = str(self.patientname).lower()
    #     path = "C:\Users\esese\Documents\\" + patient
    #     if not os.path.isdir(path): 
    #         os.makedirs(path)
    #     t = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
    #     os.makedirs(path + '\\' + t) 
    #     if os.path.exists(path + '\\' + patient + '.csv'): 
    #         with open(path + '\\' + patient +'.csv','a') as csv_file:
    #             writer = csv.writer(csv_file,  delimiter = ',')
    #             writer.writerow(['Physician Name',str(self.physicianname)])
    #             writer.writerow(['Date',(t)])

    # def collect_data(self):
    #     source1 = "C:\Users\esese\Documents\\blast-master\\kinect.csv"
    #     source2 = "C:\Users\esese\Documents\\blast-master\\imu.csv"
    #     dest = "C:\Users\esese\Documents\\" + str(self.patientname).lower() + '\\' + t 
    #     shutil.move(source1, dest)
        # shutil.move(source2, dest)
    
class MainScreen(Screen):
	pass

class ExerciseScreen(Screen):
	pass

class ListScreen(Screen): 

    def start_kinect(self):
 
        os.system('python skel.py')

    def stop_kinect(self):
        cv2.destroyAllWindows()
        
    def start_imu(self):
    
        os.system('python Hardware\SendDataTestRun.py')

    def start_parallel(self):
    
        os.system('python run_parallel.py')    

    def collect_data(self):
        global patient
        source1 = "C:\Users\esese\Documents\\blast-master\\kinect.csv"
        source2 = "C:\Users\esese\Documents\\blast-master\\imu.csv"
        source3 = "C:\Users\esese\Documents\\blast-master\\kinect.avi"

        dest = "C:\Users\esese\Documents\\" + patient + '\\' + t 
        shutil.move(source1, dest)
        shutil.move(source3, dest)
        # shutil.move(source2, dest)
 

class DropdownScreen(Screen):
    def spinner_clicked(self, value):
        kinect_graphs = ['Shoulder Angles', 'Left Elbow Angles', 'Right Elbow Angles']
        if value in kinect_graphs: 
            self.kinect_graph(value)

        imu_graphs = ['Roll', 'Pitch', 'Yaw']
        if value in imu_graphs: 
            self.imu_graph(value)

        print("Spinner Value " + value)

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

        if variable == 'Roll':
            toplot = data[:, 0]
            color = 'darkviolet'
        elif variable == 'Pitch': 
            toplot = data[:, 1]
            color = 'darkorange'
        elif variable == 'Yaw':  
            toplot = data[:, 2]
            color = 'hotpink'

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
        plt.ylabel(variable + ' (deg)')
        plt.title(variable)
        plt.legend(['Moving Average', 'Raw Data'], loc = 'best', shadow=True)
        plt.show()

    def moving_average(self, data, fs): 
        N = fs/5 # frame rate divided by five - for kinect, 200ms
        return np.convolve(data, np.ones((N,))/N, mode='valid')


    # def show_selected_value(spinner, text):
    #     print('The spinner', spinner, 'have text', text)

    # def build_data(self):
    #     spinner = Spinner(
    #         # default value shown
    #         text='Home',
    #         # available values
    #         values=('Home', 'Work', 'Other', 'Custom'),
    #         # just for positioning in our example
    #         size_hint=(None, None),
    #         size=(100, 44),
    #         pos_hint={'center_x': .5, 'center_y': .5})        

    #     spinner.bind(text=show_selected_value)
    #     runTouchApp(spinner)

class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("Main.kv")


class MainApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
	MainApp().run()
