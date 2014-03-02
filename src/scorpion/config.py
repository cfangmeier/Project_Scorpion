'''
Created on Feb 8, 2014

Configuration file for Project Scorpion. Put here anything that may be run-time dependent. 
For anything that may be sensitive(eg. passwords), just commit an empty string.

@author: caleb
'''

local_db = "project_scorpion.db"
xml_path = "localdb/default_data.xml"
scanner_path = "/dev/input/by-id/usb-HID_Keyboard_Device_HID_Keyboard_Device_Keyboard_Device-event-kbd"


pucks = {0x20:{'offset':0,'empty':0,'ratio':1},
         0x21:{'offset':0,'empty':0,'ratio':1}
        }
