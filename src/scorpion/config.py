'''
Created on Feb 8, 2014

Configuration file for Project Scorpion. Put here anything that may be run-time dependent. 
For anything that may be sensitive(eg. passwords), just commit an empty string.

@author: caleb
'''
import os
path_sep = os.path.sep
use_gui = True

project_root = path_sep.join(__file__.split(path_sep)[:-3])
drink_image_path = path_sep.join([project_root,'data','images','drinks'])
liquor_image_path = path_sep.join([project_root,'data','images','liquor'])
ingredient_image_path = path_sep.join([project_root,'data','images','ingredients'])
misc_image_path = path_sep.join([project_root,'data','images','misc'])


local_db = path_sep.join([project_root,'data','db','project_scorpion.sqlite3'])
dat_path = path_sep.join([project_root,'data','db','default.dat'])
scanner_path = "/dev/input/by-id/usb-HID_Keyboard_Device_HID_Keyboard_Device_Keyboard_Device-event-kbd"

#a setup with 16 pucks 0x20
pucks = {0x0:{'offset':0,'empty':0,'ratio':1},
         0x1:{'offset':0,'empty':0,'ratio':1},
         0x2:{'offset':0,'empty':0,'ratio':1},
         0x3:{'offset':0,'empty':0,'ratio':1},
         0x4:{'offset':0,'empty':0,'ratio':1},
         0x5:{'offset':0,'empty':0,'ratio':1},
         0x6:{'offset':0,'empty':0,'ratio':1},
         0x7:{'offset':0,'empty':0,'ratio':1},
         0x8:{'offset':0,'empty':0,'ratio':1},
         0x9:{'offset':0,'empty':0,'ratio':1},
         0xA:{'offset':0,'empty':0,'ratio':1},
         0xB:{'offset':0,'empty':0,'ratio':1},
         0xC:{'offset':0,'empty':0,'ratio':1},
         0xD:{'offset':0,'empty':0,'ratio':1},
         0xE:{'offset':0,'empty':0,'ratio':1},
         0xF:{'offset':0,'empty':0,'ratio':1}
        }
