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
import simplejson as json
from lib.utils import Utils
from lib.config import Readconfig
from lib.couch import Couch
from lib.errors import Errors

# Globals
SETTINGS_FILE_NAME = '../cfg/admin.cfg' 
OS_PATH =  os.path.dirname(os.path.realpath(__file__))                                           
settings = OS_PATH + '/' + SETTINGS_FILE_NAME

# Argument parser
parser = OptionParser()
parser.add_option("-f", "--file", 
	dest='file',
	help="Name of the ddoc file to upload")
(options, args) = parser.parse_args()
file = options.file

# Check file 
if not file:
	sys.exit("Wrong filename. Specify a .js file to upload with -f")
if not os.path.isfile(file):
	sys.exit("File not found: " + file)
if not file.endswith('js'):
	sys.exit("Wrong filename. Specify a .js file to upload with -f")

# Get filename and path
path, filename = os.path.split(file)

# Init couch connection
cfg = Readconfig().readconfig(settings)
couch = Couch(cfg)
j = couch.isAlive()
if not couch.hasDB():
	sys.exit("Missing or wrong SVT database: " + cfg.db)
	
print("\nParsing file: " + file)

# Extract info from filename
if filename.startswith('reduce_'):
	action = 'reduce'
	js = filename.replace('reduce_','')
elif filename.startswith('list_'):
	action = 'list'
	js = filename.replace('list_','')
else:
	action = 'map'
	js = filename
parts = js.replace('.js','').split('_')
ddoc = parts[0]
name = parts[1]

# Read the function file
with open(file) as f:
	func = f.read()

# Chech for existence of ddoc, view and action
try:
	r = couch.getDesignDoc(ddoc)
	# Doc was found
	j = json.loads(r)

	# Check for view
	if action == 'map' or action == 'reduce':
		if 'views' not in j:
			j['views'] = { name : { action : func }}
			didsomething = True
		elif name not in j['views']:
			j['views'][name] = { action: func}
			didsomething = True
		else:
			j['views'][name][action] = func 
			didsomething = True
	elif action == 'list':
		if 'lists' not in j:
			j['lists'] = { name : func }
			didsomething = True
		else:
			j['lists'][name] = func
			didsomething = True
	data = json.dumps(j)
	# Put the ddoc
	couch.putDesignDocString(ddoc, data)
	print("Update DDOC: " + ddoc + ", action: " + action + ", name: " + name )
					
# Doc not found, create it 
except Errors.svtError as e:
	
	if e.code == 404:
		# Compose the json around the view function
		if action == 'map' or action == 'reduce' :
			schema = { 
				"_id": '_design/' + ddoc,
				"views": {
					name: {
						action: func
					}
				},
				"language":"nodejs"
			}
		# Compose the json around the list function
		elif action == 'list' :
			schema = { 
				"_id": '_design/' + ddoc,
				"lists": {
					name: func
				},
				"language":"nodejs"
			}
		# Unkown action
		else:
			sys.exit("Unkown Action" + action)
		data = json.dumps(schema)
		# Put the ddoc
		try:
			couch.putDesignDocString(ddoc, data)
			print("Create DDOC: " + ddoc + ", action: " + action + ", name: " + name )
		except Errors.svtError as e:
			print("Code: " + str(e.code))
			print("Message: " + e.msg)
			print("Call: " + e.call)
			sys.exit(e.code)

	else:
		print("Code: " + str(e.code))
		print("Message: " + e.msg)
		print("Call: " + e.call)
		sys.exit(e.code)

except Exception:
	raise



