#!/usr/bin/env python
'''
Created on Feb 7, 2014

@author: caleb
'''

from scorpion.hal.scanner import init_scanner, stop_scanner
from scorpion.hal.puck import init_pucks
from scorpion.command import process_command
from scorpion.localdb.db import init_db, commit_db
from scorpion.ui.ui_main import run_ui

scanner_thread = None

def main_loop():
    while True:
        print('-->',end='')
        cmd = input()
        if cmd == "exit": return
        process_command(cmd)

def init_scorpion():
    global scanner_thread;
    init_db()
    init_pucks()
    init_scanner()

def close_scorpion():
    stop_scanner()
    commit_db()


if __name__ == '__main__':
    
    init_scorpion()
    run_ui()
    close_scorpion()

