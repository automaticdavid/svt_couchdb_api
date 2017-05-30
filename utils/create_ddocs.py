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

		# Extract info from filename
		if f.startswith('reduce_'):
			action = 'reduce'
			js = f.replace('reduce_','')
		elif f.startswith('list_'):
			action = 'list'
			js = f.replace('list_','')
		else:
			action = 'map'
			js = f 
		parts = js.replace('.js','').split('_')
		ddoc = parts[0]
		name = parts[1]

		# Read the function file
		didsomething = False
		with open(path) as f:
			func = f.read()

		# Chech for existence of ddoc, view or list and action
		try:
			r = couch.getDesignDoc(ddoc)
			j = json.loads(r)
			# Check for view
			if action == 'map' or action == 'reduce':
				if 'views' not in j:
					j['views'] = { name : { action : func }}
					didsomething = True
				elif name not in j['views']:
					j['views'][name] = { action: func}
					didsomething = True
				elif action not in j['views'][name]:
					j['views'][name][action] = func 
					didsomething = True
			elif action == 'list':
				if 'lists' not in j:
					j['lists'] = { name : func }
					didsomething = True
				elif name not in j['lists']:
					j['lists'][name] = func
					didsomething = True

			if didsomething:
				data = json.dumps(j)
				# Put the ddoc
				couch.putDesignDocString(ddoc, data)
				print("Update DDOC: " + ddoc + ", action: " + action + ", name: " + name )
					
		# Doc not found, create it 
		except Errors.svtError as e:

			print("Creating DDOC " + ddoc)
			
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
						"language":"javascript"
					}
				# Compose the json around the list function
				elif action == 'list' :
					schema = { 
						"_id": '_design/' + ddoc,
						"lists": {
							name: func
						},
						"language":"javascript"
					}
				# Unkown action
				else:
					sys.exit("Unkown Action" + action)
				data = json.dumps(schema)
				# Put the ddoc
				try:
					couch.putDesignDocString(ddoc, data)
					print("Create DDOC: " + ddoc + ", action: " + action + ", name: " + name )
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


