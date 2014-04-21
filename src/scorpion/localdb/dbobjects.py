'''
Created on Feb 12, 2014

@author: caleb
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship, backref
base = declarative_base()


class Brand(base):
    __tablename__ = 'brand'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    country = Column(String, nullable = False)
    

class Type(base):
    __tablename__ = 'type'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    description = Column(String, nullable = False)
    

class Liquor(base):
    __tablename__ = 'liquor'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    abv = Column(Integer, nullable = False) #0<=x<=100
    density = Column(Float, nullable = False)
    
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable = False)
    brand = relationship("Brand", backref = backref('liquors', order_by=name))
    
    type_id = Column(Integer, ForeignKey('type.id'), nullable = False)
    type = relationship("Type", backref = backref('liquors', order_by=name))
    

class LiquorSKU(base):
    __tablename__ = 'liquorsku'
    
    id = Column(Integer, primary_key = True)
    volume = Column(Float, nullable = False)
    bottleweight = Column(Float, nullable = False)
    upc = Column(String, unique=True, nullable = False)
    image = Column(String)
    
    liquor_id = Column(Integer, ForeignKey('liquor.id'))
    liquor = relationship("Liquor", backref = backref('skus'))

class Extra(base):
    __tablename__ = 'extra'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    

class Drink(base):
    __tablename__ = 'drink'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    glasstype = Column(String, nullable = False)
    description = Column(String, nullable = False)
    instructions = Column(String, nullable = False)
    image = Column(String)

class LiquorIngredient(base):
    __tablename__ = 'liquoringredient'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float, nullable = False)
    measure_unit = Column(String, nullable = False)
    
    liquor_id = Column(Integer, ForeignKey('liquor.id'))
    liquor = relationship("Liquor", backref = backref('drinks'))
    
    drink_id = Column(Integer, ForeignKey('drink.id'))
    drink = relationship("Drink", backref = backref('liquors'))
    

class GenLiquorIngredient(base):
    __tablename__ = 'genliquoringredient'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float, nullable = False)
    measure_unit = Column(String, nullable = False)
    
    type_id = Column(Integer, ForeignKey('type.id'))
    type = relationship("Type", backref = backref('drinks'))
    
    drink_id = Column(Integer, ForeignKey('drink.id'))
    drink = relationship("Drink", backref = backref('genliquors'))
    

class ExtraIngredient(base):
    __tablename__ = 'extraingredient'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float, nullable = False)
    measure_unit = Column(String, nullable = False)
    
    extra_id = Column(Integer, ForeignKey('extra.id'))
    extra = relationship("Extra", backref = backref('drinks'))
    
    drink_id = Column(Integer, ForeignKey('drink.id'))
    drink = relationship("Drink", backref = backref('extras'))
    

class LiquorInventory(base):
    __tablename__ = 'liquorinventory'
    
    id = Column(Integer, primary_key = True)
    measure = Column(Float, nullable = False) #mL
    puck_address = Column(Integer, unique = True, nullable = False)
    date_added = Column(DateTime, nullable = False)
    
    liquorsku_id = Column(Integer, ForeignKey('liquorsku.id'))
    liquorsku = relationship("LiquorSKU", backref = backref('inventory'))
    

class ExtraInventory(base):
    __tablename__ = 'extrainventory'
    
    id = Column(Integer, primary_key = True)
    
    extra_id = Column(Integer, ForeignKey('extra.id'))
    extra = relationship("Extra", backref = backref('inventory'))
    

def create_tables(engine):
    base.metadata.create_all(engine)