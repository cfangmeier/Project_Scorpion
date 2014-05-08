'''
Created on Mar 24, 2014

@author: caleb
'''
import re

from kivy.app import App
from kivy.properties import (ObjectProperty, BooleanProperty, 
                             StringProperty, ListProperty)
from kivy.lang import Builder
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

import scorpion.localdb.db as db
import scorpion.localdb.dbobjects as dbo
import scorpion.utils as utils
from scorpion.ui.add_bottle import AddBottlePopup, add_bottle_popup_open

_app = None

Builder.load_file('./ui/main_screens.kv')
Builder.load_file('./ui/add_drink_screens.kv')
Builder.load_file('./ui/add_bottle_screens.kv')

def set_upc(upc):
    if _app is not None:
        _app.scanned_upc = upc

class StartScreen_LiquorView(ButtonBehavior, BoxLayout):
    liquor_inv = ObjectProperty(None)
    def __init__(self, liquor_inv, **kwargs):
        super().__init__(**kwargs)
        self.bind(liquor_inv=self.update)
        self.liquor_inv = liquor_inv
    
    def update(self, inst, value):
        l = self.liquor_inv.liquorsku.liquor
        self.ids.display_name.text = l.brand.name + ' ' + l.name
        self.ids.display_image.source = utils.get_liquor_image_path(l)
    
    def on_release(self, *args):
        _app.get_screen('liquorscreen').liquor_inv = self.liquor_inv
        _app.set_screen('liquorscreen')

class StartScreen(Screen):
    liquor_list = ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(liquor_list=self.update)
        self.liquor_list, _ = db.get_inventory()
    
    def update(self, inst, value):
        liquor_holder = self.ids.liquor_holder
        liquor_holder.clear_widgets()
        for liquor_inv in self.liquor_list:
            sslv = StartScreen_LiquorView(liquor_inv)
            liquor_holder.add_widget(sslv)

class LiquorScreen_LiquorView(Button):
    liquor = None

class LiquorScreen_DrinkView(ButtonBehavior, BoxLayout):
    drink = ObjectProperty(dbo.Drink())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(drink=self.update)
    def update(self, inst, value):
        self.ids.drink_name.text = self.drink.name
        self.ids.drink_image.source = utils.get_drink_image_path(self.drink)
    
    def on_release(self, *args, **kwargs):
        super().on_release(*args, **kwargs)
        _app.get_screen('mixingscreen').drink = self.drink
        _app.set_screen('mixingscreen')

class LiquorScreen(Screen):
    liquor_inv = ObjectProperty(dbo.LiquorInventory())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(liquor_inv=self.update)
    
    def update(self, inst, value):
        self.ids.liquor_image.source = utils.get_liquor_image_path(self.liquor_inv.liquorsku.liquor)
        d = self.liquor_inv.date_added
        self.ids.date_added.text = "Date Added: "+'/'.join(map(str,[d.month,d.day,d.year]))
        self.ids.volume.text = str(self.liquor_inv.volume_left)+' mL Remaining'
        self.ids.brand_info.text = "Distilled By: "+self.liquor_inv.liquorsku.liquor.brand.name
        
        self.ids.drink_list.clear_widgets()
        for d in db.get_drinks_using_liquor(self.liquor_inv.liquorsku.liquor):
            lsdv = LiquorScreen_DrinkView()
            lsdv.drink = d
            self.ids.drink_list.add_widget(lsdv)
        

class MixingScreen_IngrView(Button):
    ingredient = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(ingredient=self.update)
    def update(self, *args):
        print('mixing: ',args)
        self.text = str(self.ingredient)

class MixingScreen(Screen):
    drink = ObjectProperty(dbo.Drink())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(drink=self.update)
    
    def update(self, inst, value):
        self.ids.drink_name.text = self.drink.name
        self.ids.drink_descr.text = self.drink.description
        self.ids.drink_instr.text = self.drink.instructions
        self.ids.drink_image.source = utils.get_drink_image_path(self.drink)
        
        self.ids.drink_ingr_list.clear_widgets()
        for ing in self.drink.liquors + self.drink.genliquors + self.drink.extras:
            msiv = MixingScreen_IngrView()
            msiv.ingredient = ing
            self.ids.drink_ingr_list.add_widget(msiv)
    

class DrinkSelectScreen_DrinkView(Button):
    drink = None
    
    def on_release(self, *args, **kwargs):
        super().on_release(*args, **kwargs)
        _app.get_screen('mixingscreen').drink = self.drink
        _app.set_screen('mixingscreen')

class DrinkSelectScreen(Screen):
    drink_list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(DrinkSelectScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.drink_list.clear_widgets()
        for drink in db.get_drinks():
            dssdv = DrinkSelectScreen_DrinkView()
            dssdv.text = drink.name
            dssdv.drink = drink
            self.drink_list.add_widget(dssdv)


class MainApp(App):
    show_add_bottle_popup = BooleanProperty(False)
    show_add_drink_popup = BooleanProperty(False)
    scanned_upc = StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popup = None
        self.bind(scanned_upc=self.add_new_bottle)
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen())
        self.sm.add_widget(LiquorScreen())
        self.sm.add_widget(MixingScreen())
        self.sm.add_widget(DrinkSelectScreen())
        return self.sm
    
    def set_screen(self, screen_name):
        self.sm.current = screen_name
    def get_screen(self, screen = None):
        if screen is None:
            return self.sm.current_screen
        else:
            return self.sm.get_screen(screen)
    
    def add_new_bottle(self):
        if not add_bottle_popup_open
        self.add_bottle_popup.
        
        
        
#     def add_new_bottle(self,liquorSKU):
#         l_inv = db.add_to_inventory(liquorSKU)
#         self.get_screen('startscreen').liquor_list.append(l_inv)
#         
#         self.popup.dismiss()
#         self.popup = None
#         
#         
#     def find_potential_matches(self):
#         brand = self.popup.sm.brand
#         type_ = self.popup.sm.type
#         matches = db.get_liquors(brand, type_)
#         if len(matches) == 0:
#             lcs = self.popup.sm.get_screen('liquorcreationscreen')
#             lcs.back_link = self.popup.sm.current
#             self.popup.sm.current = 'liquorcreationscreen'
#         else:
#             self.popup.sm.get_screen('liquorselectionscreen').items = matches
#             self.popup.sm.current = 'liquorselectionscreen'

def run_ui():
    global _app
    _app = MainApp()
    _app.run()
