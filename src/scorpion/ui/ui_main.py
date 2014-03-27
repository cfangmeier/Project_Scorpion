'''
Created on Mar 24, 2014

@author: caleb
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.uix.button import Button


class ScrollButton(Button):
    def __init__(self, **kwargs):
        super(ScrollButton, self).__init__(**kwargs)
    

class StartScreen(Screen):
    icon_container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
    
    def on_enter(self, *args):
        Screen.on_enter(self, *args)
        self.icon_container.add_widget(ScrollButton(text = 'hello'))

class MainApp(App):
    
    def __init__(self, **kwargs):
        super(MainApp,self).__init__(**kwargs)
    
    def on_pause(self):
        return True

if __name__ == '__main__':
    m = MainApp()
    m.run()
    