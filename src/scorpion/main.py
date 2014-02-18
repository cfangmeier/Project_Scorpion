'''
Created on Feb 7, 2014

@author: caleb
'''

import time
import multiprocessing as mp

from scorpion.localdb import db
from scorpion.hal.scanner import read_scanner

scanner_data = None

def main_loop():
    
    while True:
        time.sleep(0.2)
        if not scanner_data.empty():
            print scanner_data.get()


def init_scorpion():
    global scanner_data
    scanner_data = mp.Queue()
    scanner = mp.Process(target=read_scanner, args = [scanner_data])
    scanner.start()
    
    


if __name__ == '__main__':
    init_scorpion()
    main_loop()
