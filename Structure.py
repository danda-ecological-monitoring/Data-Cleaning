### Generic Cleaning Script for DEMP Data
#Hannah Fritsch

#Purpose 
	#Read in data
	#Convert time zones
	# Identify / flag missing data
	# initial pass at error checking

#Variable Initializaion
	#Classes to follow - This is initial needed info
	# May create class with all of these data points to make mergable later

#Critical Data
SensorType = ""
SensorName = ""
Interval = None # Critical, expected gap between data
SensorLocation = "" # May not be distinguishable from site name
Ward = ""
TimeSpan = none #Range of Time, in form (start, stop)
#may be worth making small object span
InputTimeZone = 0  # in form UTC + ITZ
DestinationTimeZone = 5.75 # Defaulting to Nepal Time
ExpectedVar = None # list of expected variables, will be mapped to sensor type
#map to be specified and stored  in secondary csv file
VariableNames = None

#Other Metadata
Title = ""
Compiler = ""
ContactInfo = ""
FileName = ""

#Reference Files To Be defined (csv)
	#Sensor Types:
		# Contains List of All Known Sensor Types
		#For each Sensor Type
			#Expected Data Frequency/ Rate
			#Expected Variable Names
			#Error Parameters for variable?
		#Use: Read in, create map of sensor type, these objects
	#List of known sites / site names / abrreviations
# Actual Data
	#Structure internal to this document, has not yet been decided
	#Maybe a list of objects
		#object consists of time, and a location for each data field
		#Has to be flexible
			#ordered list, maybe?
			#need to see if I can write code that generates object class from variable list
			#and populates the member variables
			#otherwise, have expected "object type" mapped to each sensor
		#This has the advantage of glueing the time stamp to the data, so it can't get misplaced
	#Alternative: Top level objects are variables
		# Top level metadata
			#Direct Read? Yes/ No (No indicates derived/ secondary data)
			#Functions Applied () - (Smooth, Period Average, Derivative, Standard Deviation, Other)
			#Fields Referenced (list) - written by generating function
		#Consist of a set of n-tupples, n = 3
		#ordered by first value
		#first value is time
		#second value is the actual data point
		# Third Value: Error flag set or list of possible flags true/ false
			#Values ("", "unusual", "not physically possible", "potential flat", "user flag", "other"
			#May be excessive, need concise method
			
		#Pro - May be easier to graph
			#Easier to add variables/ columns
		#Con - Extra Layers
	
	# Other important Data, to make top level or generated within function for error checking 
		#List of expected times
		#Based off Time Span and Time Interval 
	

#Read_Reference 
	#Reads in any necessary reference files
	#populates reference map
	#@Read_Reference (reference) where reference is the csv
	#or otherwise delimited text file
def Read_Reference(reference):


#Expect
	# Actually Populates key variables / member variables based on what is typical for sensor type
	#@Expect(type) where type is the sensor type
def Expect(type):



#Read_Data
	#Reads in initiial CSV file, scrapes and initializes sensor type, name, location, input time zone,
	#variable names, time span , data, and other expected metadata
	#Calls Expect(sensor type), to generate expected info about sensor type
	#Calls Read Reference
	
	#@Read(data, flag) where data is the csv file of data
def Read_Data(data, flag, reference): 
    
#Default Functions to apply to variable objects
	#Average (variable, period)
	#Standard Deviation (variable, period)
	# Numerical Derivative (variable)
	#Default Smoothing function (tenative, need parameters)
	# Potential Flatline - may need to flag on SDEV
	


