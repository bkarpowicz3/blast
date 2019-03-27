from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import kivy.uix.screenmanager
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

class LoginScreen(GridLayout):
    pass

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Physician Name'))
        self.physicianname = TextInput(multiline=False)
        self.add_widget(self.physicianname)
        self.add_widget(Label(text='Patient Name'))
        self.patientname = TextInput(multiline=False)
        self.add_widget(self.patientname)
    

class MainScreen(Screen):
	pass

class AnotherScreen(Screen):
    pass

class ExerciseScreen(Screen):
	pass

class ListScreen(Screen):
	pass
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("Main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
	MainApp().run()
	  
