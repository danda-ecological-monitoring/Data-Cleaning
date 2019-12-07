##Clean
## For now, this is a testing spot for reading in csv files
## test file is
import os
import csv
import numpy as np
import pandas as pd
import name as n
import format as f



#notes on purple air data
#minutes uptime will help find gaps: look for zeroes
	#time between data is not consistent enough to look for specific spacng
	#variable names need shortening
	#temp appears to be farenheit, needs to be changed to Celcius
	#need to establish difference between pm2.5 - which compares to laser egg
	#equivalent names on weather also good

	#humidity is other overlapping variable

#reading in purple air - hardcode for testing purposes


os.chdir('C:\\Users\\Hannah Fritsch\\Documents\\DEMP Code\\Data\\LaserEgg')
la = pd.read_csv('Ward3PNMHIairqualitydataNovember2018.csv', header = 5)
la = pd.read_csv('Ward3PNMHIairqualitydataNovember2018.csv', header = 5)

os.chdir('C:\\Users\\Hannah Fritsch\\Documents\\DEMP Code\\Data\\Weather')
weather = pd.read_csv('ward3PNMHIweatherdatafebruary2018.csv', header = 0)



def format(df,type):
	"""
	df = data frame
	type = string representing data type
	wraper for format modules master function"""
	return f.format(df, type)

def append (df, *df2):
	""" df is the intial data frame
	df2 is any additional data frames to be appended"""
	if df2:
		for i in df2:
			df = df.append(i)
	return df

def name_data (df,name):
	"""
	where name is a Name object
	wrapper for name, attaches the name of the sensor as a columns
	df is a dataframel'"""
	df['Sensor'] = name.short










