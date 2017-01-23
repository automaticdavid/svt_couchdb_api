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
from lib.utils import Utils
from lib.config import Readconfig
from lib.couch import Couch
from lib.errors import Errors

# Globals
SETTINGS_FILE_NAME = '../cfg/admin.cfg' 
DDOCS_DIR = '../ddocs/' 
OS_PATH =  os.path.dirname(os.path.realpath(__file__))                                           
settings = OS_PATH + '/' + SETTINGS_FILE_NAME
ddocsdir = OS_PATH + '/' + DDOCS_DIR

# Init couch connection
cfg = Readconfig().readconfig(settings)
couch = Couch(cfg)
j = couch.isAlive()
print(j)
if not couch.hasDB():
	sys.exit("Missing or wrong SVT database: " + cfg.db)
	
# Loop .js files
for f in sorted(os.listdir(ddocsdir)):
	
	path = ddocsdir + f

	if os.path.isfile(path) and f.endswith('js'):

		print("\nParsing file: " + f)
		didsomething = False

		# Extract info from filename
		if f.startswith('reduce_'):
			action = 'reduce'
			js = f.replace('reduce_','')
		else:
			action = 'map'
			js = f 
		parts = js.replace('.js','').split('_')
		ddoc = parts[0]
		view = parts[1]

		# Read the function file
		with open(path) as f:
			func = f.read()

		# Chech for existence of ddoc, view and action
		try:
			r = couch.getDesignDoc(ddoc)
			j = json.loads(r)
			# Check for view
			if view not in j["views"]:
				j["views"][view] = { action: func}
				didsomething = True
			# Check for action
			elif action not in j["views"][view]:
				j["views"][view][action] = func
				didsomething = True
			if didsomething:
				data = json.dumps(j)
				# Put the ddoc
				couch.putDesignDocString(ddoc, data)
				print("Update DDOC: " + ddoc + ", action: " + action + ", view: " + view )
					
		# Doc not found, create it 
		except Errors.svtError as e:
			
			if e.code == 404:
				# Compose the json around the map function
				schema = { 
					"_id": '_design/' + ddoc,
					"views": {
						view: {
							action: func
						}
					}
				}
				data = json.dumps(schema)
				# Put the ddoc
				try:
					couch.putDesignDocString(ddoc, data)
					print("Create DDOC: " + ddoc + ", action: " + action + ", view: " + view )
					didsomething = True
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

		finally:
			if not didsomething:
				print("Nothing to do")


