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
import simplejson as json
import yaml
from optparse import OptionParser
from lib.utils import Utils
from lib.config import Readconfig
from lib.couch import Couch
from lib.svt import Svt

# Globals
SETTINGS_FILE_NAME = 'cfg/config.cfg' 
OS_PATH =  os.path.dirname(os.path.realpath(__file__))                                           
settings = OS_PATH + '/' + SETTINGS_FILE_NAME


def main(f, action, client):

	# Init connections parameters
	cfg = Readconfig().readconfig(settings)

	# Init couch connection
	couch = Couch(cfg)

	# Test Welcome
	j = couch.isAlive()
	print(j)

	# Check if SVT DB exists
	if not couch.hasDB():
		sys.exit("Missing or wrong SVT database: " + cfg.db)
	
	# Load
	if action == "load":

		# Parsed arguments
		print('Action: ' + action) 
		print('File: ' + f)
		print('Client: ' + client)

		# Decorate and load
		d = Utils().decorator(f, client)
		for k,s in d.iteritems():
			try:
				couch.putString(s)
			except:
				print("Invalid JSON for CouchDB in file: " + k)
				raise

	# Report
	if action == "report":

		# Parsed arguments
		print('Action: ' + action) 
		print('Definition: ' + f)

		# Parse YAML
		h = open(f)
		y = yaml.load(h)

		reports = Utils().flatten(y)

		# Call couch for reports
		for report in reports: 
			
			# Extract parameters for the view, the hook and the object
			[client, collect, source] = report[0]
			[selector, marker] = report[1]
			
			# Key passed to the couch view: will select only given collect & client
			key = [collect, client, 0]
			r = couch.getView(source, selector, key)
			j = json.loads(r, object_hook = Svt(selector=selector, marker=marker).hook)
			
			# Deal with the results
			caller = [client, collect, source, selector, marker]
			if 'vipr' in source:

				# Get all urns as key
				rv = couch.getView('vipr-all', 'links', key)
				jv = json.loads(rv)
				
				# Generate a links dict 
				links = {}
				for row in jv['rows']:
					for link, data in row['value'].iteritems():
						viprsource = data['svt_source']
						if viprsource not in links:
							links[viprsource] = {}
						links[viprsource][link] = data

				# Step the json answer and follow all links
				for it in j['rows']:
					print(caller)
					print(it.key)
					viprsource = it.key[2]
					r = Utils().expander(it.value, viprsource, links)
					rr = Utils().expander(r, viprsource, links)
					rrr = Utils().expander(rr, viprsource, links)
					print(rrr)
					print("")



			else:
				for it in j['rows']: 
					Utils().tableizer(caller, it)




if __name__ == '__main__':

	# Argument parser
	parser = OptionParser()
	parser.add_option("-f", "--file", 
		dest='yamldef',
		help="YAML definition if the report request")
	parser.add_option("-l", "--load", 
		dest='loadfile',
		help="Collect ZIP file")
	parser.add_option("-c", "--client", 
		dest='client',
		help="Name of the client")
	(options, args) = parser.parse_args()

	# Set parsed values
 	yamldef = options.yamldef 
	loadfile = options.loadfile
	client = options.client

	# Needed arguments
	if not yamldef and not loadfile:
		sys.exit("Error: Either supply a YAML definition to report or a collect file to load\nRun with --help for help")

	# Load if needed
	if loadfile:
		if not client:
			sys.exit("Error: specifiying the client with -c is required")	
		try: 
			open(loadfile)
			main(loadfile, "load", client)
		except IOError:
			sys.exit("Error: can't read collect zip file: " + loadfile)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise

	# Call reports
	if yamldef:
		try: 
			open(yamldef)
			main(yamldef, "report", None)
		except IOError:
			sys.exit("Error: can't read YAML definition file: " + yamldef)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise








