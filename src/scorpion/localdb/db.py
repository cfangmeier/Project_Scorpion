'''
Created on Feb 7, 2014

@author: caleb
'''

import os
import sqlalchemy as sql
import sqlalchemy.orm as orm

import scorpion.config as config
import scorpion.localdb.dbobjects as dbo
import scorpion.localdb.xmlparser as xmlparser

session = None

def create_new_brand(name, country):
    brand = dbo.Brand()
    brand.name = name
    brand.country = country
    session.add(brand)
    return brand

def create_new_type(name):
    type_ = dbo.Type()
    type_.name = name
    session.add(type_)
    return type_

def create_new_liquor(type_, brand, name, abv):
    l = dbo.Liquor()
    l.abv = abv
    l.density = 1.
    l.brand = brand
    l.name = name
    l.type = type_
    session.add(l)
    return l

def create_new_liquorsku(liquor, volume, upc):
    lsku = dbo.LiquorSKU()
    lsku.liquor = liquor
    lsku.upc = upc
    lsku.volume = volume
    lsku.bottleweight = None
    session.add(lsku)
    return lsku

def create_new_liquorinventory(liquorsku, measure, puck_address):
    li = dbo.LiquorInventory()
    li.liquorsku = liquorsku
    li.measure = measure
    li.puck_address = puck_address
    session.add(li)
    return li

def get_inventory():
    inventory_liquor = session.query(dbo.LiquorInventory).all()
    inventory_extra = session.query(dbo.ExtraInventory).all()
    return (inventory_liquor, inventory_extra)

def get_drinks():
    drinks = session.query(dbo.Drink).all()
    return drinks

def get_drink(name):
    drink = session.query(dbo.Drink).filter(dbo.Drink.name == name).first()
    return drink

def get_drinks_using_liquor(liquor):
    drinks = set([d.drink for d in liquor.drinks])
    drinks.update(set([d.drink for d in liquor.type.drinks]))
    return list(drinks)

def get_drink_mix(drink, liquor_inventory = None, extra_inventory = None):
    if liquor_inventory == None:
        liquor_inventory = session.query(dbo.LiquorInventory).all()
    if extra_inventory == None:
        extra_inventory = session.query(dbo.ExtraInventory).all()
    mix = {'ingr_liquors':[],
           'ingr_genliquors':[],
           'ingr_extras' : [],
           'mis_liquors': [],
           'mis_genliquors':[],
           'mis_extras': []}
    mixable = True
    for i in drink.liquors:
        items = [l for l in liquor_inventory if l.liquorsku.liquor == i.liquor]
        if len(items) == 0:
            mix['mis_liquors'].append(i); mixable = False
        else:
            mix['ingr_liquors'].append((i,items))
            
    for i in drink.genliquors:
        items = [gl for gl in liquor_inventory if gl.liquorsku.liquor.type == i.type]
        if len(items) == 0:
            mix['mis_genliquors'].append(i); mixable = False
        else:
            mix['ingr_genliquors'].append((i,items))
    
    for i in drink.extras:
        items = [e for e in extra_inventory if e.extra == i.extra]
        if len(items) == 0:
            mix['mis_extras'].append(i); mixable = False
        else:
            mix['ingr_extras'].append(i)

    return mixable, mix

def get_drinks_mixable():
    available = []
    drinks = session.query(dbo.Drink).all()
    li = session.query(dbo.LiquorInventory).all()
    ei = session.query(dbo.ExtraInventory).all()
    for d in drinks:
        if(get_drink_mix(d,li,ei)[0]): available.append(d)
    return available

def get_brands():
    return session.query(dbo.Brand).all()

def get_types():
    return session.query(dbo.Type).all()

def get_liquors(brand = None, type_ = None):
    liquors = session.query(dbo.Liquor)
    if brand != None:
        liquors = liquors.filter(dbo.Liquor.brand == brand)
    if type_ != None:
        liquors = liquors.filter(dbo.Liquor.type == type_)
    liquors = liquors.all()
    return liquors
    

def get_with_upc(upc):
    match = session.query(dbo.LiquorSKU).filter(dbo.LiquorSKU.upc == upc).all()
    if len(match) == 0: return None
    else: return match[0]
    

def init_db(reset = False):
    global session
    if reset and os.path.exists(config.local_db):
        os.remove(config.local_db)
        print('removed old db')
    engine = sql.create_engine('sqlite:///'+config.local_db, echo = False)
    dbo.create_tables(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    if reset: 
        session.add_all(xmlparser.get_objects())
        session.commit()

def commit_db():
    global session
    if session != None:
        session.commit()
