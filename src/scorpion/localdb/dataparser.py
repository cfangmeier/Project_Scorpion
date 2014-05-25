'''
Created on May 22, 2014

@author: caleb
'''
import datetime
from collections import namedtuple

from scorpion.config import dat_path
import scorpion.localdb.dbobjects as dbo

classes = {'Brand','Type','Liquor','LiquorSKU','Extra','Drink',
           'LiquorIngredient','GenLiquorIngredient','ExtraIngredient',
           'LiquorInventory', 'ExtraInventory'}

DataObject = namedtuple('DataObject',['name','fields','children'])

def build_type(obj):
    t = dbo.Type()
    t.name = obj.fields['name']
    return t
    
def build_brand(obj):
    b = dbo.Brand()
    b.name = obj.fields['name']
    b.country = obj.fields['country']
    return b

def build_liquor(obj, types, brands):
    l = dbo.Liquor()
    l.name = obj.fields['name']
    l.density = float(obj.fields['density'])
    l.abv = int(obj.fields['abv'])
    try:
        l.brand = [b for b in brands if b.name == obj.fields['brand']][0]
    except IndexError:
        raise ValueError("Unknown brand {0}".format(obj.fields['brand']))
    try:
        l.type= [t for t in types if t.name == obj.fields['type']][0]
    except IndexError:
        raise ValueError("Unknown type {0}".format(obj.fields['type']))
    lskus = []
    for ls in obj.children:
        lsku = dbo.LiquorSKU()
        lsku.volume = ls.fields['volume']
        lsku.bottleweight = ls.fields['bottleweight']
        lsku.upc = ls.fields['upc']
        lsku.liquor = l
        lskus.append(lsku)
    return l, lskus

def build_extra(obj):
    e = dbo.Extra()
    e.name = obj.fields['name']
    return e

def build_drink(obj,extras,liquors,types):
    d = dbo.Drink()
    d.name = obj.fields['name']
    d.instructions = obj.fields['instructions']
    d.glasstype = obj.fields['glasstype']
    ings = []
    for i in obj.children:
        if i.name == "LiquorIngredient":
            ing = dbo.LiquorIngredient()
            try:
                brand,name = i.fields['liquor'].split('|')
                ing.liquor = [l for l in liquors if l.name==name and l.brand.name==brand][0]
            except IndexError:
                raise ValueError("Unknown liquor: {0}".format(i.fields['liquor']))
        elif i.name == "GenLiquorIngredient":
            ing = dbo.GenLiquorIngredient()
            try:
                ing.type = [t for t in types if t.name==i.fields['type']][0]
            except IndexError:
                raise ValueError("Unknown type: {0}".format(i.fields['type']))
        elif i.name == "ExtraIngredient":
            ing = dbo.ExtraIngredient()
            try:
                ing.extra = [e for e in extras if e.name==i.fields['extra']][0]
            except IndexError:
                raise ValueError("Unknown extra: {0}".format(i.fields['extra']))
        else:
            raise ValueError("Unknown ingredient type:{0}".format(i.name))
        m, *u = i.fields['measure'].split()
        ing.measure = float(m)
        ing.measure_unit = str.join(' ',u)
        ing.drink = d
        ings.append(ing)
    return d, ings

    
def build_extrainventory(obj, extras):
    ei = dbo.ExtraInventory()
    try:
        ei.extra = [e for e in extras if e.name == obj.fields['extra']][0]
    except IndexError:
        raise ValueError("Unknown Extra {0}".format(obj.fields['extra']))
    return ei
    
def build_liquorinventory(obj, liquorskus):
    li = dbo.LiquorInventory()
    try:
        li.liquorsku = [lsku for lsku in liquorskus if lsku.upc == obj.fields['upc']][0]
    except IndexError:
        raise ValueError("Unknown LiquorSKU with UPC {0}".format(obj.fields['upc']))
    li.volume_left = float(obj.fields['volume_left'])
    li.puck_address = int(obj.fields['puck_address'], base=16)
    li.date_added = datetime.datetime.now()
    return li

def pre_process(text):
    lines = text.splitlines()
    #Remove empty lines and comments
    lines = [line.split('#')[0].rstrip() for line in lines]
    lines = [line for line in lines if line.strip() != ""]
    return lines
    

def parse_object(lines, name):
    """
    A general parser for the .dat custom format. 
    """
    obj = DataObject(name=name,fields={},children=[])
    
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        first_word = line.split()[0]
        if first_word.endswith(":"):
            first_word = first_word[:-1]
            if first_word in classes: #object
                ob_name = first_word
                ob_data =[]
                i += 1
                while i<n and lines[i].startswith("  "):
                    ob_data.append(lines[i][2:]) #strip leading spaces
                    i += 1
                obj.children.append(parse_object(ob_data,ob_name))
            else: #field
                field_name = first_word
                colon = line.find(":")
                field_data = line[colon+1:].strip()
                i += 1
                while i<n and lines[i].startswith("  "):
                    field_data += " " + lines[i].strip()
                    i += 1
                obj.fields[field_name] = field_data
        else :
            raise ValueError("Improper syntax at {0}".format(line))
    return obj

def build_objects(root):
    """
    Specialized builder for objects from parse_objects
    """
        
    types = [build_type(obj) for obj in root.children if obj.name=="Type"]
    brands = [build_brand(obj) for obj in root.children if obj.name=="Brand"]
    
    liquors = [];
    liquorskus=[]
    for obj in root.children:
        if obj.name == "Liquor":
            l, lskus = build_liquor(obj,types,brands)
            liquors.append(l)
            liquorskus.extend(lskus)
    
    extras = [build_extra(obj) for obj in root.children if obj.name=="Extra"]
    
    drinks=[];
    ingredients=[]
    for obj in root.children:
        if obj.name == "Drink":
            d, ings = build_drink(obj,extras,liquors,types)
            drinks.append(d)
            ingredients.extend(ings)
    
    liquorinventory = [build_liquorinventory(obj,liquorskus) 
                       for obj in root.children if obj.name=="LiquorInventory"]
    extrainventory = [build_extrainventory(obj,extras) 
                      for obj in root.children if obj.name=="ExtraInventory"]
    
    objects = []
    [objects.extend(l) for l in [types,brands,liquors,liquorskus,extras,drinks,
                                 ingredients,liquorinventory,extrainventory]]
    
    return objects
    
def get_objects():
    with open(dat_path) as dat_file:
        text = dat_file.read()
        lines = pre_process(text)
        root = parse_object(lines,"Root")
        return build_objects(root)
    
if __name__ == '__main__':
    get_objects()