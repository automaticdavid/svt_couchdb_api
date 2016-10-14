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

# Module level logger
logger = logging.getLogger(__name__)      

class wrapper:

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
		key = [collect, client]
		r = couch.getReduce('admin', 'isnewcollect', key=key, group='2')
		new = json.loads(r)
		if new['rows']:
			code = 99
			msg = "Client: " + client + " already has a collect for date: " + collect
			call = "admin/isnewcollect"
			debug = [key, r, new]
			raise Errors.genError(code, msg, call, debug)

		# Decorate and load
		d = Utils().decorator(f, client)
		for k,s in d.iteritems():
			try:
				couch.putString(s)
			except :
				print("Invalid JSON for CouchDB in file: " + k)
				raise
