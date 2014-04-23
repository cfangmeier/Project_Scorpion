'''
Created on Mar 24, 2014

@author: caleb
'''
import os
import re

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

import scorpion.localdb.db as db
import scorpion.localdb.dbobjects as dbo
import scorpion.utils as utils
_app = None

def set_upc_from_scanner(upc):
    if _app is not None:
        _app.scanned_upc = upc

class StartScreen_LiquorView(Button):
    def __init__(self, liquor_inv, **kwargs):
        super().__init__(**kwargs)
        self.liquor_inv = liquor_inv
        l = liquor_inv.liquorsku.liquor
        self.text = l.brand.name + ' ' + l.name
        
    def on_release(self, *args):
        Button.on_release(self, *args)
        _app.get_screen('liquorscreen').liquor_inv = self.liquor_inv
        _app.set_screen('liquorscreen')

class StartScreen(Screen):
    liquor_list = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def update(self):
        self.liquor_list.clear_widgets()
        (inv, _) = db.get_inventory()
        for liquor_inv in inv:
            sslv = StartScreen_LiquorView(liquor_inv)
            self.liquor_list.add_widget(sslv)
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.update()

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

class UPCGetScreen(Screen):
    scanned_upc = StringProperty('')
    def __init__(self, upc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(scanned_upc=self.set_upc)
        self.scanned_upc = upc
    
    def set_upc(self, inst, value):
        self.ids.upc_input.text = self.scanned_upc
    
    def on_text(self, inst, text):
        if len(text) == 0:
            self.ids.done_button.disabled = True
        else:
            self.ids.done_button.disabled = False
    
    def done(self):
        upc = self.ids.upc_input.text
        self.ids.upc_input.text = ''
        liquorSKU = db.get_with_upc(upc)
        if liquorSKU is not None:
            _app.add_new_bottle(liquorSKU)
            return
        self.parent.upc = upc #save upc in screenmanager
        self.parent.current = 'brandselectionscreen'

class IntegerInput(TextInput):
    def on_text(self, inst, value):
        self.text = ''.join(re.findall('[0-9]+',value))
class FloatInput(TextInput):
    def on_text(self, inst, value):
        if value.count('.') > 1:
            i = value.find('.')
            value = value.replace('.','')
            value = value[:i]+'.'+value[i:]
        self.text = ''.join(re.findall('[0-9.]+',value))

class ListSelectionScreen(Screen):
    list_ = ObjectProperty(None)
    top_text = StringProperty("")
    done_disabled = BooleanProperty(True)
    items = None
    selection = None
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        if len(self.ids.list_.children) != 0: return
        for item in sorted(self.items,key=lambda x: x.name):
            tb = ToggleButton(text = self.get_item_name(item),
                              group = self.name+'button_group',
                              size_hint_y=None,
                              size_y='30')
            tb.item = item
            def enable_done(button): 
                self.done_disabled = False
                self.selection = button.item
                print(self.selection)
            tb.bind(on_release=enable_done)
            self.ids.list_.add_widget(tb)
    def get_item_name(self,item):
        return item.name

class BrandSelectionScreen(ListSelectionScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'brandselectionscreen'
        self.top_text = 'Please select the brand of your liquor.'
        self.items = db.get_brands()
    def done(self):
        self.parent.brand = self.selection
        self.parent.current = 'typeselectionscreen'
    def none(self):
        self.parent.current = 'brandcreationscreen'
    def back(self):
        self.parent.current = 'upcgetscreen'
        

class TypeSelectionScreen(ListSelectionScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'typeselectionscreen'
        self.top_text = 'Please select the type of your liquor'
        self.items = db.get_types()
    def done(self):
        self.parent.type = self.selection
        _app.find_potential_matches()
    def none(self):
        self.parent.current = 'typecreationscreen'
    def back(self):
        self.parent.current = 'brandselectionscreen'

class LiquorSelectionScreen(ListSelectionScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'liquorselectionscreen'
        self.top_text = "Is it one of these?"
    def get_item_name(self,item):
        return item.brand.name+" "+item.name
    def done(self):
        self.parent.liquor = self.selection
        self.parent.current = 'liquorskucreationscreen'
    def none(self):
        lcs = self.parent.get_screen('liquorcreationscreen')
        lcs.back_link = self.parent.current
        self.parent.current = 'liquorcreationscreen'
    def back(self):
        self.parent.current = 'typeselectionscreen'
    

class BrandCreationScreen(Screen):
    def create_brand(self,*args):
        name = self.ids.name_input.text
        country = self.ids.country_input.text
        brand = db.create_new_brand(name, country, add_to_session=False)
        self.parent.brand = brand
        self.parent.current = 'typeselectionscreen'
    def back(self):
        self.parent.current = 'brandselectionscreen'

class TypeCreationScreen(Screen):
    def create_type(self,*args):
        name = self.ids.name_input.text
        description = self.ids.description_input.text
        type_ = db.create_new_type(name, description, add_to_session=False)
        self.parent.type = type_
        _app.find_potential_matches()
    def back(self):
        self.parent.current = 'typeselectionscreen'

class LiquorCreationScreen(Screen):
    def create_liquor(self, *args):
        name = self.ids.name_input.text
        abv = int(self.ids.abv_input.text)
        l = db.create_new_liquor(self.parent.type, self.parent.brand,
                                 name, abv, add_to_session=False)
        self.parent.liquor = l
        self.parent.current = 'liquorskucreationscreen'
    def back(self):
        self.parent.current = self.back_link

class LiquorSKUCreationScreen(Screen):
    def create_liquorSKU(self, *args):
        volume = float(self.ids.volume_input.text)
        lsku = db.create_new_liquorsku(self.parent.liquor, 
                                       volume, self.parent.upc, add_to_session=False)
        for o in [lsku.liquor.brand, lsku.liquor.type, lsku.liquor, lsku]:
            db.add_object_to_session(o)
        _app.add_new_bottle(lsku)

class MainApp(App):
    show_add_bottle_popup = BooleanProperty(False)
    show_add_drink_popup = BooleanProperty(False)
    scanned_upc = StringProperty('')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popup = None
        #self.bind(show_add_bottle_popup=self.add_bottle_popup)
    
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
    
    def start_add_new_bottle(self):
        content = ScreenManager()
        [content.add_widget(w) for w in (UPCGetScreen(self.scanned_upc),
                                         BrandSelectionScreen(),TypeSelectionScreen(),
                                         LiquorSelectionScreen(),
                                         BrandCreationScreen(),TypeCreationScreen(),
                                         LiquorCreationScreen(),LiquorSKUCreationScreen())]
        self.popup = Popup(title='Add New Liquor',
                           content = content,
                           auto_dismiss = False,
                           size_hint=(0.7,0.9))
        self.popup.sm = content
        self.popup.open()
        
    def add_new_bottle(self,liquorSKU):
        db.add_to_inventory(liquorSKU)
        self.get_screen('startscreen').update()
        self.popup.dismiss()
        self.popup = None
        
        
    def find_potential_matches(self):
        brand = self.popup.sm.brand
        type_ = self.popup.sm.type
        matches = db.get_liquors(brand, type_)
        if len(matches) == 0:
            lcs = self.popup.sm.get_screen('liquorcreationscreen')
            lcs.back_link = self.popup.sm.current
            self.popup.sm.current = 'liquorcreationscreen'
        else:
            self.popup.sm.get_screen('liquorselectionscreen').items = matches
            self.popup.sm.current = 'liquorselectionscreen'

def run_ui():
    global _app
    _app = MainApp()
    _app.run()
