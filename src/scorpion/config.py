'''
Created on Feb 8, 2014

Configuration file for Project Scorpion. Put here anything that may be run-time dependent. 
For anything that may be sensitive(eg. passwords), just commit an empty string.

@author: caleb
'''
import os
path_sep = os.path.sep

project_root = path_sep.join(__file__.split(path_sep)[:-3])
drink_image_path = path_sep.join([project_root,'data','images','drinks'])
liquor_image_path = path_sep.join([project_root,'data','images','liquor'])
ingredient_image_path = path_sep.join([project_root,'data','images','ingredients'])


local_db = path_sep.join([project_root,'data','db','project_scorpion.sqlite3'])
xml_path = path_sep.join([project_root,'data','db','default_data.xml'])
scanner_path = "/dev/input/by-id/usb-HID_Keyboard_Device_HID_Keyboard_Device_Keyboard_Device-event-kbd"


pucks = {0x20:{'offset':0,'empty':0,'ratio':1},
         0x21:{'offset':0,'empty':0,'ratio':1}
        }
