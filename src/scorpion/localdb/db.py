'''
Created on Feb 7, 2014

@author: caleb
'''

import os
import sqlalchemy as sql
import sqlalchemy.orm as orm

import scorpion.config as config
import dbobjects as dbo
import xmlparser

session = None

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
            
    for i in drink.genliquor:
        items = [gl for gl in liquor_inventory if gl.liquorsku.liquor.type == i.type]
        if len(items) == 0:
            mix['mis_genliquors'].append[i]; mixable = False
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

def put_some_data(session):
    objects = xmlparser.get_objects()
    session.add_all(objects)

def init_db(reset = False):
    global session
    if reset and os.path.exists(config.local_db):
        os.remove(config.local_db)
        print 'removed old db'
    engine = sql.create_engine('sqlite:///'+config.local_db, echo = True)
    dbo.create_tables(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    if reset: 
        put_some_data(session)
        session.commit()

