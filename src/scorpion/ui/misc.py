'''
Created on May 14, 2014

@author: caleb
'''
import re
from kivy.uix.textinput import TextInput

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