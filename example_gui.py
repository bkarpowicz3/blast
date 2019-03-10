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
from xlwt import Workbook
wb = Workbook()

Window.clearcolor = (0.3, 0.1, 0.1, 0)
class LoginScreen(Screen):
    pass

    def submit_name(self):
        self.physicianname = self.physicianname_text_input.text
        self.patientname = self.patientname_text_input.text
        self.save()
        self.physicianname = ''
        self.patientname = ''


    def save(self):
    	sheet = wb.add_sheet('Sheet 1')
    	sheet.write(0,2,'Physician Name')
    	sheet.write(1,2,'Patient Name')
    	sheet.write(0,3, str(self.physicianname))
    	sheet.write(1,3, str(self.patientname))
    	wb.save(str(self.patientname) + '.xls')
 
    #     with open("Database.xls", "w") as fobj:
    #     	obj.write(0,0,'Physician Name')
    #     	obj.write(0,1,'Patient Name')
    #         #fobj.write(1,0, str(self.physicianname))
    #         #fobj.write(1,1, str(self.patientname))


    # def load(self):
    #     with open("Database.xls") as fobj:
    #         for name in fobj:
    #             self.name = name.rstrip()


    # def __init__(self, **kwargs):
    #     super(LoginScreen, self).__init__(**kwargs)
    #     self.cols = 2
    #     self.rows = 2
    #     self.paddin
    #     self.add_widget(Label(text='Physician Name'))
    #     self.physicianname = TextInput(multiline=False)
    #     self.add_widget(self.physicianname)
    #     self.add_widget(Label(text='Patient Name'))
    #     self.patientname = TextInput(multiline=False)
    #     self.add_widget(self.patientname)
    
class MainScreen(Screen):
	pass

# class AnotherScreen(Screen):
#     pass

class ExerciseScreen(Screen):
	pass

class ListScreen(Screen): 

    def start_kinect(self):
        import os 
        os.system('python skel.py')

    def stop_kinect(self):
        cv2.destroyAllWindows()
        
    def start_imu(self):
        import os
        os.system('SendDataTestRun.py')

class ScreenManagement(ScreenManager):
    pass


# class KinectScreen(Screen):
#     pass

#     def __init__(self, **kwargs): 
#         super(KinectScreen, self).__init__(**kwargs)






presentation = Builder.load_file("Main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
	MainApp().run()
	  