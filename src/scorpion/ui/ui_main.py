'''
Created on Mar 24, 2014

@author: caleb
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

import scorpion.localdb.db as db

_sm = None

class StartScreen_LiquorView(Button):
    def __init__(self, **kwargs):
        super(StartScreen_LiquorView, self).__init__(**kwargs)
        
    def on_release(self, *args):
        Button.on_release(self, *args)
        _sm.current = 'liquorscreen'
    

class StartScreen(Screen):
    liquor_list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.n = 1
    
    def on_pre_enter(self, *args):
        Screen.on_pre_enter(self, *args)
        self.liquor_list.clear_widgets()
        (inv, _) = db.get_inventory()
        for liquor_inv in inv:
            liquor = liquor_inv.liquorsku.liquor
            sslv = StartScreen_LiquorView()
            sslv.text = liquor.brand.name +', '+liquor.name
            self.liquor_list.add_widget(sslv)

class LiquorScreen_LiquorView(Button):
    pass

class LiquorScreen(Screen):
    pass

class MixingScreen(Screen):
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp,self).__init__(**kwargs)
    
    def build(self):
        global _sm
        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen())
        self.sm.add_widget(LiquorScreen())
        self.sm.add_widget(MixingScreen())
        _sm = self.sm
        return self.sm
    
    def on_pause(self):
        return True

def run_ui():
    m = MainApp()
    m.run()
