'''
Created on Feb 18, 2014

@author: caleb
'''
from __future__ import print_function
import time

import scorpion.hal.puck as puck
import scorpion.hal.scanner as scanner
import scorpion.localdb.db as db

def show_inventory(args):
    (liquor, extra) = db.get_inventory()
    print("===Liquors===")
    for l in liquor:
        print(l.liquorsku.liquor.brand.name,l.liquorsku.liquor.name, l.measure, l.puck_address)
    print("===Extras===")
    for e in extra:
        print(e.extra.name)

def check_scanner(args):
    upc = None
    if scanner.scanner_data.empty():
        print("scan something now! skipping in 5s")
        upc = scanner.scanner_data.get(True, 5)
        if upc == None: return
    else:
        upc = scanner.scanner_data.get_nowait()
    print("Scanned UPC: " + upc)
    liquorsku = db.get_with_upc(upc)
    if liquorsku == None:
        print("Congratulations! This is a new liquor type. Please provide some info for our records.")
        print("What brand is this liquor?")
        brands = db.get_brands()
        for i,b in enumerate(brands):
            print("{0}: {1}".format(i, b.name))
        print("{0}: Something else...".format(len(brands)))
        print("selection(0-{0}):".format(len(brands)))
        selection = int(raw_input())
        if selection == len(brands):
            print("Please enter some information about the brand of this liquor.")
            print("Name: ",end='')
            name = raw_input()
            print("Country: ",end='')
            country = raw_input()
            brand = db.create_new_brand(name, country)
        else:
            brand = brands[selection]
        
        print("What type is this liquor?")
        types = db.get_types()
        for i,t in enumerate(types):
            print("{0}: {1}".format(i, t.name))
        print("{0}: Something else...".format(len(types)))
        print("selection(0-{0}):".format(len(types)))
        selection = int(raw_input())
        if selection == len(types):
            print("What is the type of this liquor?")
            print("Type: ",end='')
            name = raw_input()
            type_ = db.create_new_type(name)
        else:
            type_ = types[selection]
        
        print("Is it one of these?")
        liquors = db.get_liquors(brand, type_)
        for i,l in  enumerate(liquors):
            print(str(i)+")"+l.brand.name+" | "+l.name)
        print("{0}: None of these".format(len(liquors)))
        print("selection(0-{0}):".format(len(liquors)))
        selection = int(raw_input())
        if selection != len(liquors):
            liquor = liquors[selection]
        else:
            print("Name of liquor?")
            print("Name: ",end='')
            name = raw_input()
            print("Alcohol by volume?(ABV) eg. .40")
            print("ABV: ",end='')
            abv = float(raw_input())
            liquor = db.create_new_liquor(type_,brand,name,abv)
        
        print("What is the volume of the bottle in mL. eg. 750 or 1750")
        volume = float(raw_input())
        liquorsku = db.create_new_liquorsku(liquor, volume, upc)
        
    db.create_new_liquorinventory(liquorsku, volume, puck.get_available_address())
    print("New item added to inventory! Hurrah!")
    db.commit_db()

def light_show(args):
    for _ in range(100):
        puck.set_leds(-1, False, False, False, True)
        time.sleep(0.05)
        puck.set_leds(-1, False, False, True, False)
        time.sleep(0.05)
        puck.set_leds(-1, False, True, False, False)
        time.sleep(0.05)
        puck.set_leds(-1, True, False, False, False)
        time.sleep(0.05)
    puck.kill_lights()

def list_drinks_available(args):
    drinks = db.get_drinks_mixable()
    print("You can mix these drinks. Congratulations!")
    for d in drinks:
        print("===="+d.name+"====")
        for i in d.liquors:
            print("-->",i.liquor.name, i.measure)
        for i in d.genliquors:
            print("-->",i.type.name, i.measure)
        for i in d.extras:
            print("-->",i.extra.name, i.measure)

def list_drinks_all(args):
    drinks = db.get_drinks()
    print("I have these drinks in my database.")
    for d in drinks:
        print("===="+d.name+"====")
        for i in d.liquors:
            print("-->",i.liquor.name, i.measure)
        for i in d.genliquors:
            print("-->",i.type.name, i.measure)
        for i in d.extras:
            print("-->",i.extra.name, i.measure)

def mix_drink(args):
    drink = db.get_drink(' '.join(args))
    if drink == None: 
        print("I don't know what that is...")
        return
    (mixable, mix) = db.get_drink_mix(drink)
    if not mixable:
        print("You don't got what it takes.\nYou are missing:")
        for miss in mix['mis_liquors']: print(miss.liquor.name)
        for miss in mix['mis_genliquors']: print(miss.type.name)
        for miss in mix['mis_extras']: print(miss.extra.name)
        return
    
    #TODO: allow choice when multiple matches
    puck.kill_lights()
    for l in mix['ingr_liquors']:
        address = l[1][0].puck_address
        puck.set_leds(address, False, False, False, True)
        print("BEHOLD!! : ",l[0].liquor.name); time.sleep(0.3)
    for l in mix['ingr_genliquors']:
        address = l[1][0].puck_address
        puck.set_leds(address, False, False, False, True)
        print("BEHOLD!! : ",l[0].type.name); time.sleep(0.3)
    time.sleep(2)
    puck.kill_lights()
    

def process_command(command):
    words = command.split()
    cmd = words[0]
    if cmd == 'process_command': return
    args = words[1:]
    l = globals()
    if l.has_key(cmd):
        l[cmd](args)
    else:
        print("Command " + cmd + " not found.:(")
