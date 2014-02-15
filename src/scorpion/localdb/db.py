'''
Created on Feb 7, 2014

@author: caleb
'''

import os
import sqlalchemy as sql
import sqlalchemy.orm as orm
import scorpion.config as config
import dbobjects



def get_some_data():
    vodka = dbobjects.Type();
    vodka.name = "Vodka"
    vodka.description = "In Soviet Russia, Vodka drinks you!"
    
    ruski = dbobjects.Producer()
    ruski.name = "Ruski"
    ruski.country = "Russia"
    ruski.yearfounded = 1874
    
    krogada = dbobjects.Liquor()
    krogada.abv = 0.4
    krogada.bottleweight = 35
    krogada.name = "Krogada"
    krogada.producer = ruski
    krogada.type = vodka
    krogada.density = 0.95
    krogada.upc = "659989000138"
    return krogada

def reset_db():
    if os.path.exists(config.local_db):
        os.remove(config.local_db)
    
    engine = sql.create_engine('sqlite:///scorpion.db', echo = True)
    dbobjects.create_tables(engine)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    session.add(get_some_data())
    session.commit()
    
if __name__ == "__main__":
    reset_db()
