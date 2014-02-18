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
    b.yearfounded = int(attrs['yearfounded'])
    objects.append(b)

def build_liquor(attrs):
    global objects
    l = dbo.Liquor()
    l.name = attrs['name']
    l.density = float(attrs['density'])
    l.abv = float(attrs['abv'])
    l.type = [t for t in objects 
              if type(t) == dbo.Type and t.name == attrs['type']][0]
    l.brand = [b for b in objects
               if type(b) == dbo.Brand and b.name == attrs['brand']][0]
    objects.append(l)

def build_liquorsku(attrs):
    global objects
    l = dbo.LiquorSKU()
    l.bottleweight = float(attrs["bottleweight"])
    l.volume = float(attrs['volume'])
    l.upc = attrs['upc']
    (brand,liquor) = attrs['liquor'].split('|')
    l.liquor = [l for l in objects 
                if type(l) == dbo.Liquor and l.name == liquor and l.brand.name == brand][0]
    objects.append(l)

def build_drink(attrs):
    global objects
    d = dbo.Drink()
    d.name = attrs['name']
    d.description = attrs['description']
    d.mixinstructions = attrs['mixinstructions']
    d.glasstype = attrs['glasstype']
    objects.append(d)
    
def build_liquoringredient(attrs):
    global objects
    li = dbo.LiquorIngredient()
    li.measure = float(attrs['measure'])
    li.drink = [d for d in objects if type(d) == dbo.Drink and d.name == attrs['drink']][0]
    (brand,liquor) = attrs['liquor'].split('|')
    li.liquor = [l for l in objects 
                 if type(l) == dbo.Liquor and l.name == liquor and l.brand.name == brand][0]
    objects.append(li)
    
def build_genliquoringredient(attrs):
    global objects
    gli = dbo.GenLiquorIngredient()
    gli.measure = float(attrs['measure'])
    gli.drink = [d for d in objects if type(d) == dbo.Drink and d.name == attrs['drink']][0]
    gli.type = [t for t in objects if type(t) == dbo.Type and t.name == attrs['type']][0]
    objects.append(gli)

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
    elif name == "GenLiquorIngredient":
        build_genliquoringredient(attrs)


def get_objects(path = xml_path):
    global objects
    if not os.path.exists(path): return False
    f = open(path,'r')
    data = f.read()
    f.close()
    parser = expat.ParserCreate()
    parser.StartElementHandler = start_element
    parser.Parse(data)
    
    ret = objects
    objects = []
    return ret
    
if __name__ == "__main__":
    print get_objects()