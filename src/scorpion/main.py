'''
Created on Feb 7, 2014

@author: caleb
'''

import threading
import sys

from scorpion.hal.scanner import start_scanner
from scorpion.hal.puck import init_pucks
from scorpion.command import process_command
from scorpion.localdb.db import init_db
def main_loop():
    while True:
        sys.stdout.write('-->')
        cmd = raw_input()
        if cmd == "exit": return
        process_command(cmd)

def init_scorpion():
    init_db()
    init_pucks()
    scanner = threading.Thread(target=start_scanner)
    scanner.start()

def close_scorpion():
    pass


if __name__ == '__main__':
    init_scorpion()
    main_loop()
    close_scorpion()