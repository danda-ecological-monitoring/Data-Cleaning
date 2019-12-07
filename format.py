"""format
A set of reformatting functions for data from sensors used by the 
Danda Ecological Monitoring Program. This contains all of the 
helper functions needed to standardize the data, the unique function
for each sensor, and a dictionary and wrapper function to call the 
correct method. These methods need to be passed a dataframe, read in 
is handled elsewhere

If you are not sure what to use from this module, I would reccomend 
starting with format(df, type)
"""

#The dictionary of functions will be defined at the bottom of the script



#Dependecies
import os
import pandas as pd
import sensor_detail as sd
import sensor_structure as ss
import customExceptions as ce

#*********Master Call Function
#function that takes and reformats a dataframe based upon sensor id
#format(df, type), where tyoe is a string key to the function map
def format(df, type): # this is dated, move to bottom
	"""The type keyword indicates which type of sensor the dataframe is from """
	return function_dictionary[type](df)

#*********Class definitions


#*********Helper Functions
def trim_frame(df):
	df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	return df

def prior_format(df,format):
	"""Checks if the dataframe appears to have been previously formatted
	by comparing the column names to the expected column names
	
	returns a boolean - true if previously formatted, false if not
	
	Assumes that formatting and renaming the colums are always bundled together
	
	Needs to return some sort of notification if the expected before/after columns are
	the same, because that breaks the underlying logic of this program
	In that case, will accept as "ok", but will be noisy about it
	"""
	

def column_match(df, format, expect):
	"""verbose error check function
	takes a data frame, format object, and a keyword indicating whether
	formatting is expected. 
	'unformatted' - checks for the unformatted version
	'formatted' - checks for the formatted version
	returns two value vector, where the first item is a boolean, and 
	the second is a multi line string
	returns boolean true if the columns match expectation
	returns false and returns a list of problems in the string otherwise
	default error behavior - returns false with a "could not calculate" error in
	the string  """

def get_format (key):
	"""Where the key is a string keyword passed to the dictionary under keyword
	should be able to catch errors where the keyword is wrong - 
	if keyword is correct, returns the sensor object"""
	try:
		format = sd.function_dictionary[key]
		return format
	except KeyError:
		print("""The string you are using did not register as a valid sensor type in the dictionary
		Please Try Again""","Current valid keys: " + sd.function_dictionary.keys())
		raise Error

def unchecked_format (df, format):
	""" Takes data frame df and sensor format object format
	returns the formatted data frame"""
	df = format.sensor_map(df)
	df = format.data_transform(df)
	return df
