# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

__author__ = "David CLAUVEL"
__version__ = "0.1"
__status__ = "Concept Code"

import logging
import os
import sys
from optparse import OptionParser
from lib.wrapper import Wrapper
from lib.errors import Errors


# Globals
SETTINGS_FILE_NAME = '../cfg/config.cfg' 
OS_PATH =  os.path.dirname(os.path.realpath(__file__))
settings = OS_PATH + '/' + SETTINGS_FILE_NAME


def main(f, client):

	existing = Wrapper().lister(settings)
	if client not in existing:
		sys.exit("Error: Cannot find client: " + client)
	elif date not in existing[client]:
		sys.exit("Error: Cannot find collect: " + date + " For client: " + client)
	else:
		Wrapper().deleter(settings, date, client)



	
if __name__ == '__main__':

	# Argument parser
	parser = OptionParser()
	parser.add_option("-c", "--client", 
		dest='client',
		help="Name of the client")
	parser.add_option("-d", "--date", 
		dest='date',
		help="Date of the collect")
	(options, args) = parser.parse_args()

	# Set parsed values
	client = options.client
	date = options.date

	# Test arguments
	if not client:
		sys.exit("Error: specifiying the client with -c is required")	
	if not date:
		sys.exit("Error: specifiying a date to delete with -d is required")

	# Test files
	try: 
		open(settings)
	except IOError:
		sys.exit("Error: can't read settings file: " + settings)
	
	# Delete
	try:
		main(date, client)
	except Errors.genError as e:
		print(e.msg)
		sys.exit(e.code)
	except Errors.svtError as e:
		print(e.code)
		print(e.msg)
		print(e.call)
		sys.exit(e.code)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise
