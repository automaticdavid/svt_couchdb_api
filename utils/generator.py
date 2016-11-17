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
from pprint import pprint
from optparse import OptionParser
from lib.wrapper import Wrapper
from lib.errors import Errors


# Globals
SETTINGS_FILE_NAME = '../cfg/config.cfg' 
OS_PATH =  os.path.dirname(os.path.realpath(__file__))                                           
settings = OS_PATH + '/' + SETTINGS_FILE_NAME


def main(settings, collect, client):

	res = Wrapper().generator(settings, collect, client, yamldef)
	pprint(res)

	
if __name__ == '__main__':

	# Argument parser
	parser = OptionParser()
	parser.add_option("-s", "--solutionid", 
		dest='client',
		help="Name of the client or solutionid value")
	parser.add_option("-c", "--collect", 
		dest='collect',
		help="Date of the collect as: 2016-09-12-11-45-45")
	parser.add_option("-y", "--yamldef",
		dest='yamldef',
		help="YAML definition for this generator run" )

	(options, args) = parser.parse_args()

	# Set parsed values
	collect = options.collect
	client = options.client
	yamldef = options.yamldef

	# Test input
	if not client:
		sys.exit("Error: specifiying the client with -s is required")	
	if not collect:
		sys.exit("Error: specifiying a collect date with -c YYYY-MM-DD-HH-MM-SS is required")
	if not yamldef:
		sys.exit("Error: specifiying a YAML file with -y is required")

	# Test files
	try: 
		open(yamldef)
	except IOError:
		sys.exit("Error: can't read yaml file: " + yamldef)
	try: 
		open(settings)
	except IOError:
		sys.exit("Error: can't read settings file: " + settings)
	
	# Generate
	try:
		main(settings, collect, client)
	except Errors.genError as e:
		print(e.msg)
		sys.exit(e.code)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise
