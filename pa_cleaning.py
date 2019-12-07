import os
os.chdir(r"C:\Users\Hannah Fritsch\Documents\DEMP Code")
import format as f
import sensor_detail as sd
import pandas as pd
import name
os.chdir(r"E:\DEMP Code")
temp = pd.read_csv("Parasi_Raw.csv",header = 0)
os.chdir(r"C:\Users\Hannah Fritsch\Documents\DEMP Code")

form = sd.PurpleAirFormat()
clean = f.unchecked_format(temp, form)

#name it
name.pop(r"E:\DEMP Code\dict2.csv")
lumbini = name.Name()

lumbini.from_long(province = "Province 5", district="Nawalparasi", city="Ramgram", ward= "none", site="Prithvi Chandra Hospital", sensor = "Purple Air")
clean["Sensor"]=lumbini.short# attach the name

print(clean.head())
clean.to_csv("parasi.csv")
