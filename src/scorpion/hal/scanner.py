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


_mapping = {11: '0', 2 : '1', 3 : '2',
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

def read_scanner(outqueue):
    if _scanner == None: init_scanner()
    while True:
        reading = []
        event = _scanner.read(EVENT_SIZE)
        while event:
            (_, _, type_, code, value) = struct.unpack(FORMAT, event)
            if type_ == 1 and value == 1:
                if _mapping[code] == '\0': break
                reading.append(_mapping[code])
            event = _scanner.read(EVENT_SIZE)
        outqueue.put(''.join(reading))

