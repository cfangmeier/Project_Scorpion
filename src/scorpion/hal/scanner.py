'''
Created on Feb 15, 2014

@author: caleb
'''
import struct
import os
import re
import select
from Queue import Queue

from scorpion.config import scanner_path

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

scanner_data = Queue()

_mapping = {11: '0', 2 : '1', 3 : '2',
           4 : '3', 5 : '4', 6 : '5',
           7 : '6', 8 : '7', 9 : '8',
           10: '9', 28: '\0'}
_scanner = None
kill_scanner_thread = False

def init_scanner():
    global _scanner
    if(not os.path.exists(scanner_path)):
        print "ERROR: barcode scanner not found"
        return
    event_path = os.readlink(scanner_path)
    event_id = re.findall('[0-9]+$',event_path)[-1]
    os.system("xinput float " + event_id)
    _scanner = open(scanner_path, "rb")

def start_scanner():
    global scanner_data
    if _scanner == None: init_scanner()
    while True:
        if kill_scanner_thread: return
        #print kill_scanner_thread
        (rlist,_,_) = select.select([_scanner],[],[],0.5)
        if len(rlist) == 0: continue
        reading = []
        event = _scanner.read(EVENT_SIZE)
        while event:
            (_, _, type_, code, value) = struct.unpack(FORMAT, event)
            if type_ == 1 and value == 1:
                if _mapping[code] == '\0': break
                reading.append(_mapping[code])
            event = _scanner.read(EVENT_SIZE)
        scanner_data.put(''.join(reading))

def stop_scanner():
    global kill_scanner_thread
    kill_scanner_thread = True