'''
Created on Apr 22, 2014

@author: caleb
'''
import os
import scorpion.config as config

def get_drink_image_path(drink):
    img_name = drink.name.lower().replace(' ','_')+'.png'
    img_path = os.path.join(config.drink_image_path,img_name)
    if os.path.isfile(img_path):
        return img_path
    else:
        return ""
    
def get_liquor_image_path(liquor):
    img_name = liquor.type.name.lower().replace(' ','_')+'.jpg'
    img_path = os.path.join(config.liquor_image_path,img_name)
    if os.path.isfile(img_path):
        return img_path
    else:
        return ""
    
def get_misc_image_path(misc):
    img_path = os.path.join(config.misc_image_path,misc)
    if os.path.isfile(img_path):
        return img_path
    else:
        return ""