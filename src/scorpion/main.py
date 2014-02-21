'''
Created on Feb 7, 2014

@author: caleb
'''

import threading
import sys

from scorpion.hal.scanner import start_scanner, stop_scanner
from scorpion.hal.puck import init_pucks
from scorpion.command import process_command
from scorpion.localdb.db import init_db

scanner_thread = None

def main_loop():
    while True:
        sys.stdout.write('-->')
        cmd = raw_input()
        if cmd == "exit": return
        process_command(cmd)

def init_scorpion():
    global scanner_thread;
    init_db(True)
    init_pucks()
    scanner_thread = threading.Thread(target=start_scanner)
    scanner_thread.start()

def close_scorpion():
    stop_scanner()
    scanner_thread.join()


if __name__ == '__main__':
    init_scorpion()
    main_loop()
    close_scorpion()

