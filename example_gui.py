from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import kivy.uix.screenmanager
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import cv2

class LoginScreen(Screen):
    pass

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
        
class ScreenManagement(ScreenManager):
    pass

# class NewScreen(Screen):
#     pass

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
	  