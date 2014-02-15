'''
Created on Feb 12, 2014

@author: caleb
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship, backref
base = declarative_base()


class Producer(base):
    __tablename__ = 'producer'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    country = Column(String)
    yearfounded = Column(Integer)
    

class Type(base):
    __tablename__ = 'type'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    

class Liquor(base):
    __tablename__ = 'liquor'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    abv = Column(Float)
    bottleweight = Column(Float)
    density = Column(Float)
    upc = Column(String)
    
    producer_id = Column(Integer, ForeignKey('producer.id'))
    producer = relationship("Producer", backref = backref('liquors', order_by=name))
    
    type_id = Column(Integer, ForeignKey('type.id'))
    type = relationship("Type", backref = backref('liquors', order_by=name))
    

class Extra(base):
    __tablename__ = 'extra'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    producer_id = Column(Integer, ForeignKey('producer.id'))
    producer = relationship("Producer", backref = backref('extras', order_by=name))
    

class Drink(base):
    __tablename__ = 'drink'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    glasstype = Column(String)
    description = Column(String)
    mixinstructions = Column(String)
    

class LiquorIngredient(base):
    __tablename__ = 'liquoringredient'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float)
    
    liquor_id = Column(Integer, ForeignKey('liquor.id'))
    liquor = relationship("Liquor", backref = backref('drinks'))
    
    drink_id = Column(Integer, ForeignKey('drink.id'))
    drink = relationship("Drink", backref = backref('liquors'))
    

class ExtraIngredient(base):
    __tablename__ = 'extraingredient'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float)
    
    extra_id = Column(Integer, ForeignKey('extra.id'))
    extra = relationship("Extra", backref = backref('drinks'))
    
    drink_id = Column(Integer, ForeignKey('drink.id'))
    drink = relationship("Drink", backref = backref('extras'))
    

class LiquorInventory(base):
    __tablename__ = 'liquorinventory'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float)
    
    liquor_id = Column(Integer, ForeignKey('liquor.id'))
    liquor = relationship("Liquor", backref = backref('inventory'))
    

class ExtraInventory(base):
    __tablename__ = 'extrainventory'
    
    id = Column(Integer, primary_key = True)
    
    extra_id = Column(Integer, ForeignKey('extra.id'))
    extra = relationship("Extra", backref = backref('inventory'))
    

def create_tables(engine):
    base.metadata.create_all(engine)