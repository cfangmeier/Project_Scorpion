'''
Created on Feb 7, 2014

@author: caleb
'''

import time
import multiprocessing as mp

from scorpion.localdb import db
from scorpion.hal.scanner import read_scanner

def main_loop():
    
    time.sleep(0.2)



def init_scorpion():
    scanner_data = mp.Queue()
    scanner = mp.Process(target=read_scanner, args = [scanner_data])
    scanner.start()
    
    


if __name__ == '__main__':
    init_scorpion()