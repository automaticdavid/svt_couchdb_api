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
import yaml
import simplejson as json
from lib.utils import Utils
from lib.config import Readconfig
from lib.couch import Couch
from lib.errors import Errors
from lib.svt import Svt

# Module level logger
logger = logging.getLogger(__name__)      

class Wrapper:

	# Load zip file content into CouchDB
	def loader(self, settings, f, client):

		# Init connections parameters
		cfg = Readconfig().readconfig(settings)

		# Init couch connection
		couch = Couch(cfg)

		# Test Welcome
		j = couch.isAlive()
		print(j)

		# Check if SVT DB exists
		if not couch.hasDB():
			code = 99
			msg = "Missing or wrong SVT database: " + cfg.db
			call = cfg.url
			debug = cfg
			raise Errors.genError(code, msg, call, debug)
		
		# Parsed arguments
		print('Action: Load') 
		print('File: ' + f)
		print('Client: ' + client)

		# Extract collect from zip filename
		fullname = os.path.basename(f)
		name = os.path.splitext(fullname)[0]
		collect = name.replace('output_svt_','')
		
		# Check if collect already in Couch using reduce grouping at 2
		startkey = [collect, client]
		endkey = [collect, client, {}]
		print("Checking for collect pre existence")
		r = couch.getReduce('admin', 'isnewcollect', startkey=startkey, endkey=endkey, group='2')
		new = json.loads(r)
		if new['rows']:
			code = 99
			msg = "Client: " + client + " already has a collect for date: " + collect
			call = "admin/isnewcollect"
			debug = [startkey, endkey, r, new]
			raise Errors.genError(code, msg, call, debug)

		# Decorate and create bulk json
		bulk = {}
		bulk['docs'] = [] 
		warnings =  []
		d = Utils().decorator(f, client)
		for k,s in d.iteritems():
			try:
				j = json.loads(s)
				bulk['docs'].append(j)
			except ValueError:
				warnings.append("Invalid JSON for CouchDB in file: " + k)
				raise

		# List the invalid files
		print("\n".join(warnings))
	
		# Bulk load
		try:
			data = json.dumps(bulk)
			couch.postBulk(data)
		except :
			print("Error with bulk loader")
			raise


	# Generate JSON from CouchDB and report def YAML
	def generator(self, settings, collect, client, yamldef):

		# Init connections parameters
		cfg = Readconfig().readconfig(settings)

		# Init couch connection
		couch = Couch(cfg)

		# Test Welcome
		j = couch.isAlive()
		print(j)

		# Check if SVT DB exists
		if not couch.hasDB():
			code = 99
			msg = "Missing or wrong SVT database: " + cfg.db
			call = cfg.url
			debug = cfg
			raise Errors.genError(code, msg, call, debug)
		
		# Parsed arguments
		print('Action: Generate') 
		print('Collect: ' + collect)
		print('Client: ' + client)

		# Check if collect already in Couch using reduce grouping at 2
		startkey = [collect, client]
		endkey = [collect, client, {}]
		print("Checking for collect existence")
		r = couch.getReduce('admin', 'isnewcollect', startkey=startkey, endkey=endkey, group='2')
		new = json.loads(r)
		if not new['rows']:
			code = 99
			msg = "Client: " + client + " does not have a collect for date: " + collect
			call = "admin/isnewcollect"
			debug = [startkey, endkey, r, new]
			raise Errors.genError(code, msg, call, debug)

		# Parse YAML
		h = open(yamldef)
		y = yaml.load(h)
		reports = Utils().flatten(y)

		# Structure for result json
		res = Utils().hash()

		# Call couch for reports
		for (source, selector), markers in reports.iteritems(): 
			
			# Key passed to the couch view: will select only given collect & client
			startkey = [collect, client]
			endkey = [collect, client, {}]
			c = couch.getView(source, selector, startkey, endkey)
			r = Utils().cleanKeys(c)

			# Loop over the markers
			for marker in markers:
				# Save the Caller
				caller = [client, collect, source, selector, marker]
				# Deal with the catch all special marker
				if marker == 'svt_all':
					j = json.loads(r, object_hook = Svt(selector=selector).hook_all)
				else:	
					j = json.loads(r, object_hook = Svt(selector=selector, marker=marker).hook_marker)
				# Special ViPR call
				if 'vipr' in source:
					pass
				# Update hash result 
				res = Utils().jsonify(res, caller, j)

		# Dump the hash into a json string
		s = json.dumps(res)
		return(s)

	# List all clients and collects from the Couch
	def lister(self, settings):

		# Init connections parameters
		cfg = Readconfig().readconfig(settings)

		# Init couch connection
		couch = Couch(cfg)

		# Test Welcome
		j = couch.isAlive()
		print(j)

		# Check if SVT DB exists
		if not couch.hasDB():
			code = 99
			msg = "Missing or wrong SVT database: " + cfg.db
			call = cfg.url
			debug = cfg
			raise Errors.genError(code, msg, call, debug)

		# Call reduce
		r = couch.getReduce('admin', 'isnewcollect', startkey=None, endkey=None, group='2')
		j = json.loads(r)

		# Do some formating 
		res = {}
		for row in j['rows']:
			count = row['value']
			k = row['key']
			(date, client) = k
			if client in res:
				res[client].append(date)
			else:
				res[client] = [date]
		return res

