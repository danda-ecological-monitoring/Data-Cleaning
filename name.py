"""Module: name
Hannah Fritsch
University of New Mexico,  Danda Ecological Monitoring Program, Spring 2019

This program contains a series of functions meant to create and interpret names,
and is structured according to the naming conventions for the Danda Ecological Monitoring Program

You do need to run pop() to intialize the dictionary for any of these functions to work"""
import pandas as pd
import bidict # allows a two way dictionary
from bidict import bidict
import customExceptions

conventions = """ """

####################################################################################################
####################################################################################################
#Initializing objects, constants, definitions
###########################

## Create the libraries needed - long hand on the right, short hand as key (on left, first)
## Seperate libraries are needed forr each field. Initialized here
province_dictionary = bidict()
district_dictionary  = bidict()
city_dictionary  = bidict()
ward_dictionary  = bidict ()
site_dictionary  = bidict()
sensor_dictionary  = bidict()
data_dictionary  = bidict() #data title with description, mostly ignored


select  = {
"""a map of keywords to dictionary objects
 can be expanded to deal with case sensitivity"""
	'province':province_dictionary ,
	'district':district_dictionary ,
	'city':city_dictionary ,
	'ward':ward_dictionary ,
	'site':site_dictionary ,
	'sensor':sensor_dictionary ,
	'data': data_dictionary
	}
######################################################################################################
######################################################################################################
#Class definitions
##########
class Name:
	""" Stores the short version of a sensor name, paired with all the longhand components
	Can be written to by providing all of the longhands or the short string
	name.from_short (short_name) , OR name.from_long (pr, di, ci, w, si, se)
	While it is possible to directly edit the individual member variables
	it is strongly reccomended that you only use the included class functions
	to edit the contents """
	def __init__ (self):
		self.short = ''
		self.province = ''
		self.district = ''
		self.city = ''
		self.ward = ''
		self.site = ''
		self.sensor = ''

	def from_short (self,short_name):
		"""from_short (self, short_name)
		short_name = the condensed version of a sensor name
		Takes the short version of a name and populates all the
		member variables of the object"""
		self.short = short_name.strip()
		self.temp = read(short_name)
		self.province = temp[0]
		self.district = temp[1]
		self.city = temp[2]
		self.ward = temp[3]
		self.site = temp[4]
		self.sensor = temp[5]

	def from_long (self,province, district, city, ward, site, sensor):
		"""from_long (self,province, district, city, ward, site, sensor)
		takes the long components of a sensor name, and
		populates the member variables of the object"""
		self.province = province.strip()
		self.district = district.strip()
		self.city = city.strip()
		self.ward = ward.strip()
		self.site = site.strip()
		self.sensor = sensor.strip()
		self.short = write(province, district, city, ward, site, sensor)

	def copy (self, name2):
		"""copy (self,name2)
		where name2 is another name object
		copies the parameters from another name object to self"""
		self.province = name2.province
		self.district = name2.district
		self.city = name2.city
		self.ward = name2.ward
		self.site = name2.site
		self.sensor = name2.sensor
		self.short = name2.short


##################################################################################################
#Functions
##########


def pop (file):
	"""pop (file)
	Reads in a csv file, and populates the naming libraries
		Expected CSV format: 3 rows; cat, short, long   (category, short, long)
	Category identifies which dictionary the entry belongs in
	Headers expected in first row of file (otherwise, will drop first entry)"""
	s = pd.read_csv(file)
	t = s.columns.values
	for i in s.index:
		pop_help(s[t[0]][i].strip(), s[t[1]][i].strip(), s[t[2]][i].strip())
		#^removes spaces on the ends of the strings before passing them


def pop_help (category, short, long):
	"""pop_help (category, short, long)
	category = category, should match key in select dictionary ,
	short = shortened version of field, long = full version
	helper function that takes a category, shorthand, and
	longhand, and updates appropriate dictionary"""
	select.get(category).put(short,long)

def save_dictionaries(file):
    """Takes the name of the csv file to save the dictionary to, and saves the
    dictionaries
    Eventually - update to save to sql """



def read (name):
	""" read (name)
	interprets name, which is a sensor name
	returns an 6 element array containing, in order
	province, district, city, ward, site, sensor
	inverse of write"""
	temp = name.split('.')
	parts = temp[0].split('_')
	province = province_dictionary [parts[0]]
	district = district_dictionary [parts[1]]
	city = city_dictionary [parts[2]]
	ward = ward_dictionary [parts[3]]
    site = site_dictionary [parts[4]]
	sensor = sensor_dictionary [parts[5]]

	return [province, district, city, ward, site, sensor]



def write_csv (name):
	"""write_csv (name)
	takes name object, attaches a file ending """
	a = name.short
	return a+'.csv'


def write(province, district, city, ward, site, sensor):
    """write(province, district, city, ward, site, sensor)
    Takes the long version of the 6 components of a sensor name
    returns a condensed string"""
try:
        pro = province_dictionary .inv[province.strip()]
        dis = district_dictionary .inv[district.strip()]
        cit = city_dictionary .inv[city.strip()]
        war = ward_dictionary .inv[ward.strip()]
        sit = site_dictionary .inv[site.strip()]
        sen = sensor_dictionary .inv[sensor.strip()]

        out = pro+'_'+dis+'_'+cit+'_'+war+'_'+sit+'_'+sen
        return out
    except KeyError as e:
        print(e)


##############################################################################
### Functions for User input/ interaction
def update_dictionary(dictionary):
    """A function that takes a dictionary, then asks the user to input a new
    short/long pair  """


def choose_name_input(dictionary):
    """ A function that prompts the user to select a key from dictionary
    returns the longhand value"""

def short_input():
    """ Walks user through inputing the short name to name a sensor
    handles some errors
    returns a name object"""
    input = input("Please enter the shorthand sensor name: ")
    name = Name()
    try: # try passing this to the name function
        name.from_short(input.strip())
        return(name)
    except Exception as e: #there are a range of possibilities here
        print(e)

def long_input():
    """ Walks user through inputting a sensor name the long way
    handles sme errors, returns a name object"""


def input_name():
    """ A function that takes user input for name definitions step by step
    Should be run after the dictionaries are initialized
    Returns a name object"""
    response = ""
    name = Name()
    while response not in ["yes", "no"]:
        response = input("Do you already know the condensed sensor name? \nyes/no\n").strip().lower()
    if response == "yes":
        short = input("Please enter sensor name: \n").strip() # need a  helper to check for valid sensor name
        try: #placeholder error catching
            name.from_short(short) #break into subfunction to loop whole yes routine
        except:
            print("That is an invalid name")




