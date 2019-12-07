"""Custom exceptions for the DEMP data management code base"""

class UnexpectedColumnError(Exception):
	"""Raised when a dataframe passed has a problematic unexpected column"""
	pass


class MissingColumnError(Exception):
	"""Raised when a dataframe passed is missing an expected column """
	pass


class PreviousFormatError(Exception):
	"""Raised when a data frame passed to a formatting function
	appears to have been previously formatted
	Included because running certain helper functions like unit
	conversions or timezone adjustments
	over the data multiple times will destroy the data"""
	pass

class NotInDictionaryError(KeyError):
	"""At least one value given is not a key in the dictionary """
	pass

class DictionaryNotPopulated(NotInDictionaryError):
    """At least one of the dictionaries is not populated"""
    pass