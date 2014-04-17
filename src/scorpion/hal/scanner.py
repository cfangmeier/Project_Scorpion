'''
Created on Feb 15, 2014

@author: caleb
'''
import struct
import os
import re
import select
import threading
from queue import Queue

from scorpion.config import scanner_path

FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

scanner_data = Queue()

_mapping = {11: '0', 2 : '1', 3 : '2',
           4 : '3', 5 : '4', 6 : '5',
           7 : '6', 8 : '7', 9 : '8',
           10: '9', 28: '\0'}
_scanner_file = None
_scanner_thread = None
kill_flag = False

def init_scanner():
    global _scanner_file, _scanner_thread
    if(not os.path.exists(scanner_path)):
        print("ERROR: barcode scanner not found")
        return
    #disconnect scanner from x-input so scans
    #aren't fed to wherever the cursor is
    event_path = os.readlink(scanner_path)
    event_id = re.findall('[0-9]+$',event_path)[-1]
    os.system("xinput float " + event_id)
    _scanner_file = open(scanner_path, "rb")
    _scanner_thread = threading.Thread(target=_run)
    _scanner_thread.start()

def _run():
    global scanner_data
    while True:
        if kill_flag: return
        (rlist,_,_) = select.select([_scanner_file],[],[],0.5)
        if len(rlist) == 0: continue
        reading = []
        event = _scanner_file.read(EVENT_SIZE)
        while event:
            (_, _, type_, code, value) = struct.unpack(FORMAT, event)
            if type_ == 1 and value == 1:
                if _mapping[code] == '\0':
                    _scanner_file.read(EVENT_SIZE)
                    _scanner_file.read(EVENT_SIZE)
                    break
                reading.append(_mapping[code])
            event = _scanner_file.read(EVENT_SIZE)
        scanner_data.put(''.join(reading))

def stop_scanner():
    global kill_flag, _scanner_thread
    kill_flag = True
    if _scanner_thread != None:
        _scanner_thread.join()
    