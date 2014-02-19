'''
Created on Feb 18, 2014

@author: caleb
'''
import time

import scorpion.hal.puck as puck
import scorpion.localdb.db as db

def show_inventory(args):
    (liquor, extra) = db.get_inventory()
    for l in liquor:
        print l.liquorsku.liquor.name, l.measure
    for e in extra:
        print e.extra.name

def check_scanner(args):
    print 'checking scanner'

def light_show(args):
    for _ in range(100):
        puck.set_leds('20', False, False, False, True)
        time.sleep(0.05)
        puck.set_leds('20', False, False, True, False)
        time.sleep(0.05)
        puck.set_leds('20', False, True, False, False)
        time.sleep(0.05)
        puck.set_leds('20', True, False, False, False)
        time.sleep(0.05)

def list_drinks_available(args):
    print 'list drinks'

def list_drinks_all(args):
    print 'list drinks all'

def mix_drink(args):
    print 'mixing a drink'

def process_command(command):
    words = command.split()
    cmd = words[0]
    if cmd == 'process_command': return
    args = words[1:]
    l = globals()
    if l.has_key(cmd):
        l[cmd](args)
    else:
        print "Command " + cmd + "not found.:("
