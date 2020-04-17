#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Hannah Fritsch
#
# Created:     20/02/2020
# Copyright:   (c) Hannah Fritsch 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os

import getpass as gp
import sys
import pandas as pd

def bulk_upload(path, domain,db,tab,file, user, password):
    """The domain is the domain or ip of server
    bb is relevant database
    tab is the relevanant table name
    file is the name of a csv file"""

    os.chdir(path)

    df =file

    #create the engine
    engine = sql.create_engine("mysql://"+user+":"+password+"@"+domain+"/"+db)
    connection = engine.connect()
    metadata = sql.MetaData()
    table= sql.Table(tab, metadata, autoload=True, autoload_with=engine)

    script= text("""load data local infile "{df}"
    IGNORE
    into table {tab}
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\\r'
    IGNORE 1 LINES;""".format(df= df, tab=tab, db = db))

    script2=text("""
    delete from {tab}
    Where Sensor = '';""".format(df= df, tab=tab, db = db))

    #print(script)
    connection.execute(text("SHOW SESSION VARIABLES LIKE 'wait_timeout';"))
    connection.execute(script)
    connection.execute(text("set SQL_SAFE_UPDATES = 0"))
    connection.execute(script2)
    connection.execute(text("set SQL_SAFE_UPDATES = 1"))

def get_sensor_dict(domain,db,tab, user, password):
    '''Returns a dictionary that maps between the Purple air name for a sensor,
    and our database key for said sensor
    In the case of our database, this is meant to pull the Name and ID columns
    frrom Site_list
    '''
    #create the engine
    engine = sql.create_engine("mysql://"+user+":"+password+"@"+domain+"/"+db)
    connection = engine.connect()
    metadata = sql.MetaData()
    table= sql.Table(tab, metadata, autoload=True, autoload_with=engine)

    query= text("""Select Name, ID from {tab}""".format(tab=tab, db = db))

    result = connection.execute(query)
    diction = {}
    for row in result:
        diction[row[0]] = row[1]

    return diction





def main():
    pass

if __name__ == '__main__':
    main()
