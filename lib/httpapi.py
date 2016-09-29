# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

__author__ = "David CLAUVEL"
__version__ = "0.1"
__status__ = "Concept Code"
	 
import requests
import sys
from lib.errors import Errors
	
class HTTPApi:

	def __init__(self, host, port, username, password, debug):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.debug = debug

	def get(self, uri):
		try:
			headers = {'Content-type':'text/json', 'Accept':'application/json'} 
			url = self.host + ':' + self.port + uri
			r = requests.get(url, headers = headers)
			if r.status_code == 200:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
			
	def put(self, uri, params = None, data = None):
		try:
			headers = {'Content-type':'text/json', 'Accept':'application/json'} 
			url = self.host + ':' + self.port + uri
			r = requests.put(url, headers = headers, params = params, data = data)
			if r.status_code < 400:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		
	def delete(self, uri, params = None, data = None):
		try:
			headers = {'Content-type':'text/json', 'Accept':'application/json'} 
			url = self.host + ':' + self.port + uri
			r = requests.delete(url, headers = headers, params = params, data = data)
			if r.status_code < 400:
				return r.json()
			else:
				raise Errors.svtError(r, url)
		except requests.exceptions.Timeout as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.TooManyRedirects as e:
			print(e)
			if self.debug == False:
				sys.exit(1)
		except requests.exceptions.RequestException as e:
			print(e)
			if self.debug == False:
				sys.exit(1)