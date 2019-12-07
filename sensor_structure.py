#In this file, I am going to define several classes. 
#The top level is an abstract 'sensor'that contains 3 main class level components
#A list of expected input columns
#A list of expected output columns
# A map between the two (exception needed for name column)
#and an instance level field
#optional: instance level field to store current data frame. Undecided at moment
#instance level - input time zone - initialized to a class level default

#important methods/ functions
# check list of columns from a data frame against expected input
# ditto output


# I will then create an extension class for each sensor,
#with the constant 

# This file will be called by the format file, and/or an intermediary

#This is the abstract layer, specifics will be in sensor_detail

##########################################################################################################
#General Class Definitions ###############################################################################
class ExpectedColumns():
	def __init__ (self,column_set):
		self.columns = set(column_set)
	
	
	def missing(self, df):
		""" returns a set of columns missing from the dataframe
		"Sensor" is excepted from this"""
		df_columns = set(df.columns)
		return self.columns - df_columns - {'Sensor'}


	def unexpected (self, df):
		"""returns set of unexpected columns found in data frame 
		"Sensor" is excepted from this"""
		df_columns = set(df.columns)
		return df_columns - self.columns - {'Sensor'}
		
	def match (self,df):
		"""checks to see if dataframe df columns match expected
		returns boolean 
		may be updated to output what exactly doesn't match
		"Sensor" is excepted from this"""
		df_columns = set(df.columns)- {'Sensor'}
		return df_columns == self.columns
	
	
class SensorFormat():
	"""Please do not put methods in the specific sensor classes
	Add here where all the child classes can inherit"""
	raw_columns = ExpectedColumns({})
	formatted_columns = ExpectedColumns({})
	column_map = {}
	time_zone = ""
	sensor_key = ""  # The name key for the sensor type
	
	@classmethod
	def data_transform(self,df):
		"""run this immediately after map
		any functions that affect the data points directly go here
		for most of these, it will be critical not to accidentally run twice"""

	@classmethod 
	def sensor_map(self,df):
		""" This should always be coupled with data_transform, and called  that
		but after checks for prior cleaning		"""
		df = df.rename(index = str, columns = self.column_map)
		return df