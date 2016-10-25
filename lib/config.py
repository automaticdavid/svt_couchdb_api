# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

__author__ = "David CLAUVEL"
__version__ = "v1.0"
__status__ = "Production Code"

import configparser

class Configuration:

	def __init__(self, host, port, username, password, debug, db, verify):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.debug = debug		
		self.db = db
		self.verify = verify 


class Readconfig:

	def readconfig(self,configfilename):
		config = configparser.RawConfigParser()
		try:
			with open(configfilename, 'r') as configfile:
				config.readfp(configfile)

			host = None
			port = None
			username = None
			password = None
			db = None
			debug = False
			verify = False

			envname = "COUCHDB"
			if not config.has_section(envname):
				raise 
			else:
				host = config.get(envname,'host')
				port = config.get(envname,'port')
				username = config.get(envname,'username')
				password = config.get(envname,'password')
				debug = config.get(envname,'debug')
				db = config.get(envname,'db')
				s_verify = config.get(envname,'verify')
				if s_verify == 'False':
					verify = False
				else:
					verify = True
		except:
			raise
				
		return Configuration(host, port, username, password, debug, db, verify)
		
		
		
