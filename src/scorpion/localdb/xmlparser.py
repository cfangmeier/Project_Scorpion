'''
Created on Feb 17, 2014

@author: caleb
'''
import os
import xml.parsers.expat as expat

from scorpion.config import xml_path
import dbobjects as dbo
objects = []

def build_type(attrs):
    global objects
    t = dbo.Type()
    t.name = attrs['name']
    t.description = attrs['description']
    objects.append(t)
    
def build_brand(attrs):
    global objects
    b = dbo.Brand()
    b.name = attrs['name']
    b.country = attrs['country']
    b.yearfounded = attrs['yearfounded']
    objects.append(b)

def build_liquor(attrs):
    global objects
    b = dbo.Liquor()
    b.name = attrs['name']
    b.density = attrs['density']
    b.abv = attrs['abv']
    b.bottleweight = attrs['bottleweight']
    b.upc = attrs['upc']
    b.type = [t for t in objects 
              if type(t) == dbo.Type and t.name == attrs['abv']][0]

def start_element(name, attrs):
    
    if name == "Type":
        build_type(attrs)
    elif name == "Brand":
        build_brand(attrs)
    elif name == "Liquor":
        build_liquor(attrs)
    elif name == "Drink":
        build_drink(attrs)
    elif name == "LiquorIngredient":
        build_liquoringredient(attrs)


def get_objects():
    if not os.path.exists(xml_path): return False
    f = open(xml_path,'r')
    data = f.read()
    f.close()
    parser = expat.ParserCreate()
    parser.StartElementHandler = start_element
    parser.Parse(data)
    
    
if __name__ == "__main__":
    get_objects()