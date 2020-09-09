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
from db_connect import bulk_upload, get_sensor_dict
import getpass as gp
from tkinter import Tk, filedialog
import tkinter as tk

######Initializing login variables
domain = ""
database = ""
user = ""
password = ""
data_path = ""

#################################################################################################
#################################################################################################
#USER INPUTS

####


########
##OTHER INPUTS


################################################################################################
################################################################################################
#CONSTANTS (regex)
#file strings for unaveraged data
purple = r".+[(].+[)]\s[(].+[)](\s\S+){5}[.]csv"
purpleA = ".+\s[(].*side[)]\s[(].+[)](\s\S+){5}[.]csv" # could maybe be less explicit
purpleB = ".+\sB\s[(]undefined[)]\s[(].+[)](\s\S+){5}[.]csv"

#primary v secondary
primary = "[\D|\d]+([(].+[)]\s){2,2}Primary"
secondary ="[\D|\d]+([(].+[)]\s){2,2}Secondary"

sensor_map = ""
sensor_key = "Sensor"



################################################################################################
################################################################################################
### FUNCTIONS
def main():
    ###GUI

    # layout constants
    padding = 5
    root = tk.Tk()
    entry_width = 30
    
    entries = tk.Frame(root)
    buttons = tk.Frame(root)
    header = tk.Frame(root)

    #### key variable definitions
    domain_ent = tk.Entry(entries, width = entry_width)
    database_ent = tk.Entry(entries, width = entry_width)
    user_ent = tk.Entry(entries,width = entry_width)
    password_ent = tk.Entry(entries, show = "*",width = entry_width)
    
    head_text= tk.Label(header, text = "Login for Air Quality Database", \
                    pady = padding, padx = padding, font = "TKdefaultfont 15")
    
    
    def login():
        global domain, database,user,password,data_path
        domain = domain_ent.get()
        database = database_ent.get()
        user = user_ent.get()
        password = password_ent.get()
        data_path = filedialog.askdirectory(title = "Please indicate where the data is located")
        upload()
    
    submit = tk.Button(buttons, text = "Submit" , command = login)
    help_button = tk.Button(buttons, text = "Help")
    about = tk.Button(buttons, text = "About")

    header.grid(row = 0)
    
    head_text.grid()
    
    entries.grid(row = 1)
    
    tk.Label(entries, text="Database").grid(row=1, sticky = 'E')
    tk.Label(entries, text="Domain").grid(row=2, sticky = 'E')
    tk.Label(entries, text="User").grid(row=3, sticky = 'E')
    tk.Label(entries, text="Password").grid(row=4, sticky = 'E')
    
    buttons.grid(row = 2)
    
    database_ent.grid(row=1, column=1, pady = padding, padx = padding, columnspan = 2)
    domain_ent.grid(row=2, column=1, pady = padding, padx = padding,  columnspan = 2) 
    user_ent.grid(row=3, column=1, pady = padding, padx = padding,  columnspan = 2)
    password_ent.grid(row=4, column=1, pady = padding, padx = padding,  columnspan = 2)
    submit.grid(row = 5, column = 1, pady = padding, padx= padding)


def upload():
    global sensor_map
    sensor_map = get_sensor_dict(domain,database,"Site_List", user, password)
    #structure of key: (fuunction reference, format object, table)
    #where table is representd as a string
    table_map = {"a_primary":(a_primary,sd.PurpleAirFormat,"PurpleAir","temp_table_1.csv"),\
                "a_secondary":(a_secondary,sd.PA_A_Secondary,"PA_A_Secondary","temp_table_2.csv"),\
                "b_primary":(b_primary,sd.PA_B_Primary,"PA_B_Primary","temp_table_3.csv"),\
                "b_secondary":(a_secondary,sd.PA_B_Secondary,"PA_B_Secondary", "temp_table_4.csv")}

    os.chdir(data_path)
    all_files = os.listdir(data_path)

    site_set = set()

    #select channel a files to pull site names
    for file in all_files:
        if is_Purple(file) and is_B(file):
            name = regex.split("\sB\s[(]undefined[)]\s[(].+[)](\s\S+){5}[.]csv",file)[0].strip()
            site_set.add(name)

    # LIST DETECTED SITES
    print("\nList of all detected sites:")
    if len(site_set)== 0:
        print('The program detects no files')
    else:
        print("detected sites")
        print(site_set)

    type_set = table_map.values()
    for thing in type_set:
        process_upload(thing, site_set, all_files)

#############################################################################################################
#### HELPER FUNCTIONS
def process_upload(typo, site_set, file_list):
    """Where type is an object from table_map, and this finds all associated
    data, cleans it, and uploads to the appropriate table. No return
    Also adds hour and date columns to the file before upload"""
    out_file = typo[3]
    for site in site_set: 
        new_data = typo[0](site, file_list,typo[1]())

    #see what is in site set
    print("\nFor table " + typo[2] + ":")

        #loop over the site set
    full_file = None
    for site in site_set:
        print("processing " + site)
        site_file = typo[0](site,file_list,typo[1]())
        if not(site_file is None):
            if full_file is None:
                full_file = site_file
            else:
                full_file = full_file.append(site_file)
        else:
            print("No file detected for "+site) 

    #output file if possible
    if not(full_file is None):
        full_file['Hour'] = pd.DatetimeIndex(full_file['Time']).hour  # adding an hour and date column
        full_file['Date'] = pd.DatetimeIndex(full_file['Time']).date
        full_file.to_csv(out_file, index = False)
        bulk_upload(data_path, domain, database, typo[2], out_file, user, password)
    else:
        print("No cleaned data to upload. If data was expected, please check that names match")




def a_primary(name, file_list, form):
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
    clean = f.unchecked_format(df, form)
    return clean

def a_secondary(name, file_list, form):
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
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean

def b_primary(name, file_list, form):
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
    clean = f.unchecked_format(df, form)
    clean[sensor_key] = sensor_map[name]
    return clean

def b_secondary(name, file_list, form):
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
    #account for parentheses
    regname = regex.sub('[)]','[)]',regex.sub('[(]', '[(]',name))
    subset = exp_Matches (regname, files)
    #verify correct file type
    subset = exp_Matches(purple,subset)
    #further subset to primary
    subset = exp_Matches(primary,subset)
    return subset

def get_Secondary (name, files):
    """ Given the cleaned site name, and a list of files
    this returns a list that contains
    the primary files for the sensor."""
    regname = regex.sub('[)]','[)]',regex.sub('[(]', '[(]',name))
    subset = exp_Matches (regname, files)
    #verify correct file type
    subset = exp_Matches(purple,subset)
    #further subset to primary
    subset = exp_Matches(secondary,subset)
    return subset


if __name__ == '__main__':
    main()
