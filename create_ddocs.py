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
SETTINGS_FILE_NAME = 'cfg/config.cfg' 
DDOCS_DIR = 'ddocs/' 
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
for js in os.listdir(ddocsdir):
	path = ddocsdir + js
	if os.path.isfile(path) and js.endswith('js'):

		# Extract info from filename
		parts = js.replace('.js','').split('_')
		ddoc = parts[0]
		view = parts[1]

		# Read the function file
		with open(path) as f:
			func = f.readlines()

		# Chech for existence of ddoc
		try:
			j = couch.getDesignDoc(ddoc)


		except Exception as e:
			# Create ddoc 
			if e.code == 404:
				# Compose the json around the map function
				schema = { 
					"_id": ddoc,
					"views": {
						view: {
							"map": func
						}
					}
				}
				data = json.dumps(schema)
				# Put the ddoc
				couch.putDesignDocString(ddoc, data)
				


				
				

				
			

			# Other couch error






# 		with open(js) as f:
#     		func = f.readlines()
# 		json = { 
# 				"_id": ddoc_id,  
# 				"views": {


# 				}

# 			}


# 				{
#    "_design/example",
#   "views" : {
#     "foo" : {
#       "map" : "function(doc){ emit(doc._id, doc._rev)}"
#     }
#   }
# }