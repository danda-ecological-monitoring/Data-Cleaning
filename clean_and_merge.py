#-------------------------------------------------------------------------------
# Name:        merge_and_clean
# Purpose:
#
# Author:      Hannah Fritsch
#
# Created:     14/02/2020
# Copyright:   (c) Hannah Fritsch 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
""" This current version is only going to cover raw data from A-primary
looks at download folder
selects all A-primaries
cleans and names each, before merging them together
outputs a csv for upload

will only name ones already in the dictionary of sensor names - commas in ones
not in the dictionay may cause parsing errors on upload - if this is a persistent
problem, semi-colon delimited may be more appropriate

Cobbles together code from data_cleaning.py, format, and sensor_details. Presumes
formal naming has already been done, as has development of the cleaning functions"""
import pandas as pd
import format as f
import sensor_detail as sd
import os
import regex
from db_connect import bulk_upload
import getpass as gp

#input
sensor_dict = r"C:\Users\Hannah Fritsch\Documents\DEMP_Code\sensor_dict.txt" # this is a map of sensor names and ids
data_path = r"C:\Users\Hannah Fritsch\Documents\DEMP_Code\Download" #location of files
out_file = "temp_upload.csv" # output file name
# if file path not included, places cleaned file with data

#database details
domain = "econandstuff.com"
database ="demp"
table = "PurpleAir"

#login details
user = gp.getpass(prompt = "User:")
password = gp.getpass(prompt = "Password:") #do NOT hardcode.

#constants (regex)
#copied from data_cleaning_raw in geog
#file strings for unaveraged data
purple = r".+[(].+[)]\s[(].+[)](\s\S+){5}[.]csv"
purpleA = ".+\s[(].*side[)]\s[(].+[)](\s\S+){5}[.]csv" # could maybe be less explicit
purpleB = ".+\sB\s[(]undefined[)]\s[(].+[)](\s\S+){5}[.]csv"

#primary v secondary
primary = "[\D|\d]+([(].+[)]\s){2,2}Primary"
secondary ="[\D|\d]+([(].+[)]\s){2,2}Secondary"

temp_map = pd.read_csv(sensor_dict, sep = ';')
sensor_map = dict(zip(temp_map["Sensor Name"],temp_map["ID"]))
sensor_key = "Sensor"


### Functions
def main():
    os.chdir(data_path)
    all_files = os.listdir(data_path)

    site_set = set()

    #select channel a files to pull site names
    #update site_set
    for file in all_files:
        if is_Purple(file) and not(is_B(file)):
            name = file.split(" (")[0]
            site_set.add(name)

    #loop over the site set
    full_file = None
    for site in site_set:
        site_file = a_primary(site,all_files)
        if not(site_file is None):
            if full_file is None:
                full_file = site_file
            else:
                full_file = full_file.append(site_file)

    #output file if possible
    if not(full_file is None):
        full_file.to_csv(out_file, index = False)
    bulk_upload(data_path, domain, database, table, out_file, user, password)


## New Helpers


def a_primary(name, file_list):
    """takes a site name, identifies a primary, and reads it in
    formats/ cleans the data, then
    goes ahead and adds the sensor name while a it. """
    #id a primary and read in
    prime = get_Primary(name, file_list)
    #identify a and b
    #assume no duplicates
    a =exp_Matches(purpleA, prime)[0]
    df = pd.read_csv(a)
    df = f.trim_frame(df)
    form = sd.PurpleAirFormat()
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean

def a_secondary(name, file_list):
    """takes a site name, identifies a secondary, and reads it in
    formats/ cleans the data, then
    goes ahead and adds the sensor name while a it. """
    #id a primary and read in
    prime = get_Secondary(name, file_list)
    #identify a and b
    #assume no duplicates
    a =exp_Matches(purpleA, prime)[0]
    df = pd.read_csv(a)
    df = f.trim_frame(df)
    form = sd.PurpleAirFormat() # needs to be updated
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean

def b_primary(name, file_list):
    """takes a site name, identifies a primary, and reads it in
    formats/ cleans the data, then
    goes ahead and adds the sensor name while a it. """
    #id a primary and read in
    prime = get_Primary(name, file_list)
    #identify a and b
    #assume no duplicates
    a =exp_Matches(purpleB, prime)[0]
    df = pd.read_csv(a)
    df = f.trim_frame(df)
    form = sd.PurpleAirFormat() #needs to be updated
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean

def b_secondary(name, file_list):
    """takes a site name, identifies a primary, and reads it in
    formats/ cleans the data, then
    goes ahead and adds the sensor name while a it. """
    #id a primary and read in
    prime = get_Secondary(name, file_list)
    #identify a and b
    #assume no duplicates
    a =exp_Matches(purpleB, prime)[0]
    df = pd.read_csv(a)
    df = f.trim_frame(df)
    form = sd.PurpleAirFormat() #needs to be updated
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean
###############################################################################
## Helper Functions copied from data_cleaning.py, modified as needed

def is_Outdoor(file):
    """ takes an "A" file name from a sensor, and
    determines whether or not the sensor is outdoor.
    Returns boolean - true if outdoor
    defaults to false in case of error"""
    loc = False
    sub = file.split("(")[1]
    sub = sub.split(")")[0]
    if sub == "outside":
        loc = True
    return loc

def is_Purple(file_name):
    """ A function that takes a file name, and checks if it follows the naming
    conventions for tthe purple air sensor
    returns a boolean
    """
    return bool(regex.fullmatch(purple, file_name))

def is_B(file_name):
    """ A function that takes a file name, and checks if it follows the naming
    conventions for tthe purple air sensor b
    returns a boolean
    """
    return bool(regex.fullmatch(purpleB, file_name))

def exp_Matches (regx, file_list):
    """ Takes a regular expression and a list of strings
    returns a subset list of strings that match the expression"""
    subset = []
    for file in file_list:
        if regex.match(regx,file):
            subset.append(file)
    return subset

def get_Primary (name, files):
    """ Given the cleaned site name, and a list of files
    this returns a list that contains
    the primary files for the sensor."""
    subset = exp_Matches (name, files)
    #verify correct file type
    subset = exp_Matches(purple,subset)
    #further subset to primary
    subset = exp_Matches(primary,subset)
    return subset

def get_Secondary (name, files):
    """ Given the cleaned site name, and a list of files
    this returns a list that contains
    the primary files for the sensor."""
    subset = exp_Matches (name, files)
    #verify correct file type
    subset = exp_Matches(purple,subset)
    #further subset to primary
    subset = exp_Matches(secondary,subset)
    return subset


if __name__ == '__main__':
    main()
