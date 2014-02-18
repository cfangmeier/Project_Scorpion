'''
Created on Feb 7, 2014

@author: caleb
'''

import os
import sqlalchemy as sql
import sqlalchemy.orm as orm

import scorpion.config as config
import dbobjects
import xmlparser


def put_some_data(session):
    objects = xmlparser.get_objects()
    session.add_all(objects)

def reset_db():
    if os.path.exists(config.local_db):
        os.remove(config.local_db)
        print 'removed old db'
    
    engine = sql.create_engine('sqlite:///'+config.local_db, echo = True)
    dbobjects.create_tables(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    put_some_data(session)
    session.commit()
    
if __name__ == "__main__":
    reset_db()
