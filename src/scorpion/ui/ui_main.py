'''
Created on Mar 24, 2014

@author: caleb
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

import scorpion.localdb.db as db

_app = None

class StartScreen_LiquorView(Button):
    def __init__(self, liquor_inv, **kwargs):
        super(StartScreen_LiquorView, self).__init__(**kwargs)
        self.liquor_inv = liquor_inv
        l = liquor_inv.liquorsku.liquor
        self.text = l.brand.name + ' ' + l.name
        
        
    def on_release(self, *args):
        Button.on_release(self, *args)
        _app.get_screen('liquorscreen').current_liquor = self.liquor_inv
        _app.set_screen('liquorscreen')

class StartScreen(Screen):
    liquor_list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        Screen.on_pre_enter(self, *args)
        self.liquor_list.clear_widgets()
        (inv, _) = db.get_inventory()
        for liquor_inv in inv:
            sslv = StartScreen_LiquorView(liquor_inv)
            self.liquor_list.add_widget(sslv)

class LiquorScreen_LiquorView(Button):
    liquor = None

class LiquorScreen_DrinkView(Button):
    drink = None

class LiquorScreen(Screen):
    drink_list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(LiquorScreen,self).__init__(**kwargs)
        self.current_liquor = None
    
    def on_pre_enter(self, *args):
        
        self.drink_list.clear_widgets()
        for d in db.get_drinks_using_liquor(self.current_liquor.liquorsku.liquor):
            lsdv = LiquorScreen_DrinkView(text = d.name)
            self.drink_list.add_widget(lsdv)
        

class MixingScreen(Screen):
    drink = None

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
    
    def set_screen(self, screen):
        if type(screen) is str:
            self.sm.current = screen
        else:
            self.sm.current_screen = screen
    def get_screen(self, screen = None):
        if screen is None:
            return self.sm.current_screen
        else:
            return self.sm.get_screen(screen)

def run_ui():
    global _app
    _app = MainApp()
    _app.run()
