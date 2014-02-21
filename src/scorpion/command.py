'''
Created on Feb 18, 2014

@author: caleb
'''
import time

import scorpion.hal.puck as puck
import scorpion.localdb.db as db

def show_inventory(args):
    (liquor, extra) = db.get_inventory()
    print "===Liquors==="
    for l in liquor:
        print l.liquorsku.liquor.name, l.measure
    print "===Extras==="
    for e in extra:
        print e.extra.name

def check_scanner(args):
    print 'checking scanner'

def light_show(args):
    for _ in range(100):
        puck.set_leds(32, False, False, False, True)
        time.sleep(0.05)
        puck.set_leds(32, False, False, True, False)
        time.sleep(0.05)
        puck.set_leds(32, False, True, False, False)
        time.sleep(0.05)
        puck.set_leds(32, True, False, False, False)
        time.sleep(0.05)

def list_drinks_available(args):
    drinks = db.get_drinks_mixable()
    print "You can mix these drinks. Congratulations!"
    for d in drinks:
        print "===="+d.name+"===="
        for i in d.liquors:
            print "-->",i.liquor.name, i.measure
        for i in d.genliquors:
            print "-->",i.type.name, i.measure
        for i in d.extras:
            print "-->",i.extra.name, i.measure

def list_drinks_all(args):
    drinks = db.get_drinks()
    print "I have these drinks in my database."
    for d in drinks:
        print "===="+d.name+"===="
        for i in d.liquors:
            print "-->",i.liquor.name, i.measure
        for i in d.genliquors:
            print "-->",i.type.name, i.measure
        for i in d.extras:
            print "-->",i.extra.name, i.measure

def mix_drink(args):
    drink = db.get_drink(' '.join(args))
    if drink == None: 
        print "I don't know what that is..."
        return
    (mixable, mix) = db.get_drink_mix(drink)
    if not mixable:
        print "You don't got what it takes."
        print "You are missing:"
        for miss in mix['mis_liquors']: print miss.liquor.name
        for miss in mix['mis_genliquors']: print miss.type.name
        for miss in mix['mis_extras']: print miss.extra.name
        return
    
    #TODO: allow choice when multiple matches
    puck.kill_lights()
    for l in mix['ingr_liquors']:
        address = l[1][0].puck_address
        puck.set_leds(address, False, False, False, True)
        print "BEHOLD!! : ",l[0].liquor.name; time.sleep(0.3)
    for l in mix['ingr_genliquors']:
        address = l[1][0].puck_address
        puck.set_leds(address, False, False, False, True)
        print "BEHOLD!! : ",l[0].type.name; time.sleep(0.3)
    

def process_command(command):
    words = command.split()
    cmd = words[0]
    if cmd == 'process_command': return
    args = words[1:]
    l = globals()
    if l.has_key(cmd):
        l[cmd](args)
    else:
        print "Command " + cmd + " not found.:("
