'''
Created on May 22, 2014

@author: caleb
'''
import re

#import scorpion.localdb.dbobjects as dbo
from scorpion.config import dat_path
classes = {'Brand','Type','Liquor','LiquorSKU','Extra','Drink',
           'LiquorIngredient','GenLiquorIngredient','ExtraIngredient',
           'LiquorInventory', 'ExtraInventory'}




def get_objects(text):
    lines = text.splitlines()
    #remove empty lines
    lines = [line for line in lines if line.strip() != ""]
    #remove any line comments
    lines = [line.split('#')[0] for line in lines]
    
    objects = []
    object_lines = ""
    object_ = ""
    for line in lines:
        line = line.rstrip()
        if line[:-1] in classes: #start of object
            objects.append((object_,object_lines))
            object_lines = []
            object_ = line[:-1]
        else:
            object_lines.append(line)
    objects.append((object_,object_lines))
    objects = objects[1:]
    for object_ in objects:
        print(object_)
            
    

if __name__ == '__main__':
    with open(dat_path) as dat_file:
        text = dat_file.read()
        print(get_objects(text))

