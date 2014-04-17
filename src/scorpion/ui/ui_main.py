'''
Created on Mar 24, 2014

@author: caleb
'''
import os

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty

import scorpion.localdb.db as db
import scorpion.config as config
_app = None

class StartScreen_LiquorView(Button):
    def __init__(self, liquor_inv, **kwargs):
        super().__init__(**kwargs)
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
        super().__init__(**kwargs)
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.liquor_list.clear_widgets()
        (inv, _) = db.get_inventory()
        for liquor_inv in inv:
            sslv = StartScreen_LiquorView(liquor_inv)
            self.liquor_list.add_widget(sslv)

class LiquorScreen_LiquorView(Button):
    liquor = None

class LiquorScreen_DrinkView(Button):
    drink = None
    
    def on_release(self, *args, **kwargs):
        super().on_release(*args, **kwargs)
        _app.get_screen('mixingscreen').drink = self.drink
        _app.set_screen('mixingscreen')

class LiquorScreen(Screen):
    drink_list = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_liquor = None
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.drink_list.clear_widgets()
        for d in db.get_drinks_using_liquor(self.current_liquor.liquorsku.liquor):
            lsdv = LiquorScreen_DrinkView(text = d.name)
            lsdv.drink = d
            self.drink_list.add_widget(lsdv)
        

class MixingScreen_IngrView(Button):
    pass

class MixingScreen(Screen):
    drink = None
    
    drink_name = ObjectProperty(None)
    drink_image = ObjectProperty(None)
    drink_descr = ObjectProperty(None)
    drink_instr = ObjectProperty(None)
    drink_ingr_list = ObjectProperty(None)
    
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.drink_name.text = self.drink.name
        self.drink_descr.text = self.drink.description
        self.drink_instr.text = self.drink.instructions
        img_path = os.path.join(config.drink_image_path,
                                self.drink.name.lower().replace(' ','_')+'.jpg')
        if os.path.isfile(img_path):
            self.drink_image.source = img_path
        else:
            self.drink_image.source = ""
        self.drink_ingr_list.clear_widgets()
        for li in self.drink.liquors:
            msiv = MixingScreen_IngrView()
            l = li.liquor
            msiv.text = ' '.join((l.brand.name, l.name))
            self.drink_ingr_list.add_widget(msiv)
        for gl in self.drink.genliquors:
            msiv = MixingScreen_IngrView()
            t = gl.type
            msiv.text = t.name
            self.drink_ingr_list.add_widget(msiv)
        for e in self.drink.extras:
            msiv = MixingScreen_IngrView()
            msiv.text = e.extra.name
            self.drink_ingr_list.add_widget(msiv)


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

class UPCGetPopupContent(BoxLayout):
    upc = ''

class BrandSelectionScreen(Screen):
    brand_list = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.brand_list.clear_widgets()
        for b in sorted(db.get_brands(),key = lambda x: x.name):
            tb = ToggleButton(text = b.name,
                              group = 'brand_sel_group',
                              size_hint_y=None,
                              size_y='30')
            def enable_done(*args): self.done_button.disabled = False
            tb.bind(on_press=enable_done)
            self.brand_list.add_widget(tb)

class TypeSelectionScreen(Screen):
    type_list = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def create_new_brand(self):
        pass
    def use_brand(self):
        pass
    
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        self.type_list.clear_widgets()
        for t in sorted(db.get_types(),key = lambda x: x.name):
            tb = ToggleButton(text = t.name,
                              group = 'type_sel_group',
                              size_hint_y=None,
                              size_y='30')
            def enable_done(*args): self.done_button.disabled = False
            tb.bind(on_press=enable_done)
            self.type_list.add_widget(tb)

class MainApp(App):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen())
        self.sm.add_widget(LiquorScreen())
        self.sm.add_widget(MixingScreen())
        self.sm.add_widget(DrinkSelectScreen())
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
    
    def check_upc(self, popup):
        upc = popup.content.upc
        liquorsku = db.get_with_upc(upc)
        if liquorsku is not None:
            db.add_to_inventory(liquorsku)
            return
        content = ScreenManager()
        content.add_widget(BrandSelectionScreen())
        popup = Popup(title='Add New Liquor',
                      content = content,
                      auto_dismiss = False,
                      size_hint=(0.7,0.9))
        content.popup = popup
        popup.open()

    def get_upc(self):
        content = UPCGetPopupContent()
        popup = Popup(title='Input UPC',
                      content=content,
                      auto_dismiss = False,
                      size_hint=(0.8, 0.8))
        content.popup = popup
        popup.bind(on_dismiss = self.check_upc)
        popup.open()
    

def run_ui():
    global _app
    _app = MainApp()
    _app.run()
