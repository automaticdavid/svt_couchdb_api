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
import simplejson as json
from lib.cdbapi import CouchResponse

# Module level logger
logger = logging.getLogger(__name__)               

class Couch:

	def __init__(self, cfg):
		self.couch = CouchResponse(cfg)
		self.db = cfg.db

	# Test get
	def isAlive(self):
		j = self.couch.get('/')
		return(j['couchdb'])

	# Test if DB is defined
	def hasDB(self):
		try:
			j = self.couch.get('/' + self.db)
			if j['db_name']:
				return True
			elif j['error']:
				return False
			else:
				raise Exception("Error finding SVT DB: " + self.db)
		except:
			return False

	# Create client DB
	def putDB(self, dbname):
		j = self.couch.put('/' + dbname)
		return(j)

	# Put JSON file 
	def putDoc(self, filename):
		db = self.db
		# get new uuid
		j = self.couch.get('/_uuids')
		uuid = j['uuids'][0]
		url = '/' + db +'/' + uuid
		# open file to load json
		handle = open(filename,'r')
		j_file = json.load(handle)
		data = json.dumps(j_file)
		# put document
		j = self.couch.put(url, None, data)
		return(j)
	
	# Put JSON string 
	def putString(self, s):
		db = self.db
		# get new uuid
		j = self.couch.get('/_uuids')
		uuid = j['uuids'][0]
		url = '/' + db +'/' + uuid
		# put document
		j = self.couch.put(url, None, s)
		return(j)

	# Delete all docs except _design
	def delAllDocs(self):
		db = self.db
		url = '/' + db + '/_all_docs?endkey="_design"'
		j = self.couch.get(url)
		for doc in j['rows']:
			id = doc['id']
			rev = doc['value']['rev']
			print(id, rev)
			url = '/' + db + '/'+ id
			params = {'rev' : rev } 
			r = self.couch.delete(url, params)

	# Call an existing view
	def getView(self, ddoc, view = '', startkey = None):
		db = self.db
		url = '/' + db + '/_design/' + ddoc + '/_view/' + view
		if startkey:
			# encoding is handled by the requests module
			url += '?startkey=' + json.dumps(startkey)
		j = self.couch.get(url)
		return(json.dumps(j))

	# Call an existing design doc
	def getDesignDoc(self, ddoc):
		db = self.db
		url = '/' + db + '/_design/' + ddoc 
		j = self.couch.get(url)
		return(json.dumps(j))

	# Call an existing design doc
	def putDesignDocString(self, ddoc, data):
		db = self.db
		url = '/' + db + '/_design/' + ddoc 
		j = self.couch.put(url, None, data)
		return(json.dumps(j))








