import re

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.properties import (StringProperty, ObjectProperty,
                             BooleanProperty)

import scorpion.localdb.db as db

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

add_bottle_process = None

class AddBottleProcess:
    def __init__(self):
        self.content = ScreenManager()
        screens = [UPCGetScreen(self.scanned_upc),
                   BrandSelectionScreen(), TypeSelectionScreen(),
                   LiquorSelectionScreen(), BrandCreationScreen(),
                   TypeCreationScreen(), LiquorCreationScreen(),
                   LiquorSKUCreationScreen()]
        for screen in screens:
            self.content.add_widget(screen)
        self.popup = None
        
        global add_bottle_process 
        add_bottle_process = self
        
    def open(self):
        self.popup = Popup(title="Add Bottle to Inventory!",
                           content = self.content,
                           auto_dismiss = False,
                           size_hint = (0.7, 0.9))
        
        
    def dismiss(self):
        super().dismiss()
        global add_bottle_popup_open
        add_bottle_popup_open = False
        
