'''
Created on Feb 15, 2014

@author: caleb
'''
import struct
import os
import re

from scorpion.config import scanner_path

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)


mapping = {11: '0', 2 : '1', 3 : '2',
           4 : '3', 5 : '4', 6 : '5',
           7 : '6', 8 : '7', 9 : '8',
           10: '9', 28: '\0'}

_scanner = None


def init_scanner():
    global _scanner
    if(not os.path.exists(scanner_path)):
        print "ERROR: barcode scanner not found"
        return
    event_path = os.readlink(scanner_path)
    event_id = re.findall('[0-9]+$',event_path)[-1]
    os.system("xinput float " + event_id)
    _scanner = open(scanner_path, "rb")

def close_scanner():
    global _scanner
    if _scanner != None:
        _scanner.close()
        _scanner = None

def read_scanner():
    if _scanner == None: init_scanner()
    reading = []
    
    event = _scanner.read(EVENT_SIZE)
    while event:
        (_, _, type_, code, value) = struct.unpack(FORMAT, event)
        
        if type_ == 1 and value == 1:
            if mapping[code] == '\0': break
            reading.append(mapping[code])
            
        event = _scanner.read(EVENT_SIZE)
    return ''.join(reading)


if __name__ == '__main__':
    while True:
        print read_scanner()
