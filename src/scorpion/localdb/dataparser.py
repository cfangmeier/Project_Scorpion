'''
Created on May 22, 2014

@author: caleb
'''
from collections import namedtuple
from scorpion.config import dat_path
import scorpion.localdb.dbobjects as dbo

classes = {'Brand','Type','Liquor','LiquorSKU','Extra','Drink',
           'LiquorIngredient','GenLiquorIngredient','ExtraIngredient',
           'LiquorInventory', 'ExtraInventory'}

DataObject = namedtuple('DataObject',['name','fields','children'])

def pre_process(text):
    lines = text.splitlines()
    #Remove empty lines and comments
    lines = [line for line in lines if line.strip() != ""]
    lines = [line.split('#')[0].rstrip() for line in lines]
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
            raise ValueError("Improper syntax at \"{1}\""%line )
    return obj

def build_type(obj):
    t = dbo.Type()
    t.name = obj.fields['name']
    t.description = obj.fields['description']
    return t
    
def build_brand(obj):
    b = dbo.Brand()
    b.name = obj.fields['name']
    b.country = obj.fields['country']
    return b

def build_liquor(obj):
    l = dbo.Liquor()
    l.name = obj.fields['name']
    l.density = float(obj.fields['density'])
    l.abv = int(obj.fields['abv'])

def build_liquorsku(attrs):
    global objects
    lsku = dbo.LiquorSKU()
    lsku.bottleweight = float(attrs["bottleweight"])
    lsku.volume = float(attrs['volume'])
    lsku.upc = attrs['UPC']
    (brand,liquor) = attrs['liquor'].split('|')
    lsku.liquor = [l for l in objects 
                if type(l) == dbo.Liquor and l.name == liquor and l.brand.name == brand][0]
    objects.append(lsku)

def build_liquorinventory(attrs):
    global objects
    l = dbo.LiquorInventory()
    for lsku in objects:
        if type(lsku) != dbo.LiquorSKU: continue
    l.liquorsku = [lsku for lsku in objects
                   if type(lsku) == dbo.LiquorSKU and lsku.upc == attrs['liquorsku']][0]
    l.volume_left = float(attrs['volume_left'])
    l.puck_address = int(attrs['puck_address'], base=16)
    l.date_added = datetime.datetime.now()
    objects.append(l)

def build_drink(attrs):
    global objects
    d = dbo.Drink()
    d.name = attrs['name']
    d.description = attrs['description']
    d.instructions = attrs['instructions']
    d.glasstype = attrs['glasstype']
    objects.append(d)
    
def build_liquoringredient(attrs):
    global objects
    li = dbo.LiquorIngredient()
    (measure, li.measure_unit) = attrs['measure'].split()
    li.measure = float(measure)
    li.drink = [d for d in objects if type(d) == dbo.Drink and d.name == attrs['drink']][0]
    (brand,liquor) = attrs['liquor'].split('|')
    li.liquor = [l for l in objects 
                 if type(l) == dbo.Liquor and l.name == liquor and l.brand.name == brand][0]
    objects.append(li)
    
def build_genliquoringredient(attrs):
    global objects
    gli = dbo.GenLiquorIngredient()
    (measure, gli.measure_unit) = attrs['measure'].split()
    gli.measure = float(measure)
    gli.drink = [d for d in objects if type(d) == dbo.Drink and d.name == attrs['drink']][0]
    gli.type = [t for t in objects if type(t) == dbo.Type and t.name == attrs['type']][0]
    objects.append(gli)

def build_extra(attrs):
    global objects
    e = dbo.Extra()
    e.name = attrs['name']
    objects.append(e)
    
def build_extraingredient(attrs):
    global objects
    ei = dbo.ExtraIngredient()
    (measure, ei.measure_unit) = attrs['measure'].split()
    ei.measure = float(measure)
    ei.drink = [d for d in objects if type(d) == dbo.Drink and d.name == attrs['drink']][0]
    ei.extra = [e for e in objects if type(e) == dbo.Extra and e.name == attrs['extra']][0]
    objects.append(ei)

def build_extrainventory(attrs):
    global objects
    ei = dbo.ExtraInventory()
    ei.extra = [e for e in objects if type(e) == dbo.Extra and e.name == attrs['extra']]
    objects.append(ei)


def build_objects(root):
    """
    Specialized builder for objects from parse_objects
    """
    g = globals()
    builders = {class_: g['build_'+class_.lower()] for class_ in classes}
    #linkers = {class_: g['link_'+class_.lower()] for class_ in classes}
    objects = {class_:[] for class_ in classes}
    for obj in root.children:
        objects[obj.name].append(builders[obj.name](obj))
        
    

def get_objects(text):
    lines = pre_process(text)
    root = parse_object(lines,"Root")
    return build_objects(root)
            
    

if __name__ == '__main__':
    with open(dat_path) as dat_file:
        text = dat_file.read()
        print(get_objects(text))

