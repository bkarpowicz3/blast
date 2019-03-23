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
import cv2
import xlwt 
import os
from xlwt import Workbook
import datetime
import csv
import shutil

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

        dest = "C:\Users\esese\Documents\\" + patient + '\\' + t 
        shutil.move(source1, dest)
        # shutil.move(source2, dest)
    
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("Main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
	MainApp().run()
