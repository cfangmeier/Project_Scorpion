'''
Created on Feb 7, 2014

@author: caleb
'''

import sqlalchemy as sql
import dbobjects






def init_db(filename):
    sql.create_engine('sqlite:///scorpion.db', echo = True)
