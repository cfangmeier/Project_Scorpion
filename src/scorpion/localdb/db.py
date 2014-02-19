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

