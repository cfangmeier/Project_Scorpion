'''
Created on Mar 24, 2014

@author: caleb
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)
    

class StartScreen(Screen):
    icon_container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.n = 1
    
    def on_pre_enter(self, *args):
        Screen.on_pre_enter(self, *args)
        self.icon_container.clear_widgets()
        for _ in range(10):
            self.icon_container.add_widget(ScrollButton(text = 'hello'+str(self.n)))
            self.n += 1

class LiquorScreen(Screen):
    pass

class MixingScreen(Screen):
    pass

class MainApp(App):
    
    def __init__(self, **kwargs):
        super(MainApp,self).__init__(**kwargs)
    
    def on_pause(self):
        return True

if __name__ == '__main__':
    m = MainApp()
    m.run()
    