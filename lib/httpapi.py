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
import requests
import sys
from lib.errors import Errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	
# module level logger
logger = logging.getLogger(__name__)

class HTTPApi:

	def __init__(self, host, protocol, port, username, password, debug, db, verify):
		self.host = host
		self.protocol = protocol
		self.port = port
		self.username = username
		self.password = password
		self.debug = debug
		self.db = db
		self.verify = verify

	def get(self, uri, cookie):
		try:
			headers = {'Accept':'application/json',\
				'X-CouchDB-WWW-Authenticate': 'Cookie', 'Content-Type': 'application/x-www-form-urlencoded'}
			url = self.protocol + '://' + self.host + ':' + self.port + uri
			logger.debug('GET : %s', url)
			r = requests.get(url, headers = headers, verify = self.verify, cookies = cookie)
			if r.status_code == 200:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			if self.debug == False:
				sys.exit(1)
			
	def put(self, uri, params = None, data = None):
		try:
			headers = {'Content-type':'text/json', 'Accept':'application/json'} 
			url = self.protocol + '://' + self.host + ':' + self.port + uri
			r = requests.put(url, headers = headers, params = params, data = data, verify = self.verify)
			if r.status_code < 400:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			if self.debug == False:
				sys.exit(1)
		
	def delete(self, uri, params = None, data = None):
		try:
			headers = {'Content-type':'text/json', 'Accept':'application/json'} 
			url = self.protocol + '://' + self.host + ':' + self.port + uri
			r = requests.delete(url, headers = headers, params = params, data = data, verify = self.verify)
			if r.status_code < 400:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			if self.debug == False:
				sys.exit(1)

	def post(self, uri, params = None, data = None, header = None ) :
		try:
			if header == "cookie":
				headers = {'Content-type':'application/x-www-form-urlencoded'}
			else:
				headers = {'Content-type':'application/json', 'Accept':'application/json'}
			r = requests.post(uri, headers = headers, params = params, data = data, verify = self.verify)
			if r.status_code < 400 and header == "cookie":
				jar = r.cookies
				if len(jar) != 1:
					code = 99
					msg = "Anormal number of cookies returned"
					call = "POST: " + url
					debug = (r, jar)
				else:
					for c in jar:
						cookie = {c.name: c.value}
						return(cookie)
			elif r.status_code < 400:
				return r.json()
			else:
				raise Errors.svtError(r, uri)
		except requests.exceptions.Timeout as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			if self.debug == False:
				sys.exit(1)





