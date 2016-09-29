# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

import logging
from lib.httpapi import HTTPApi 
from lib.errors import Errors

__author__ = "David CLAUVEL"
__version__ = "0.1"
__status__ = "Concept Code"


# module level logger
logger = logging.getLogger(__name__)


class CouchResponse:

	def __init__(self, config):
		self.httpapi = HTTPApi(config.host, config.port, config.username, config.password, config.debug)
		
	def get(self, uri):
		logger.debug('URI : %s', uri)
		try:
			response = self.httpapi.get(uri)
			return response
		except Errors.svtError as e:
			print("Error: ", e.code, e.msg, e.call)
			raise

	def put(self, uri, params = None, data = None):
		logger.debug('URI : %s', uri)
		try:
			response = self.httpapi.put(uri, params, data)
			return response
		except Errors.svtError as e:
			print("Error: ", e.code, e.msg, e.call)
			raise
	
	def delete(self, uri, params = None, data = None):
		logger.debug('URI : %s', uri)
		try:
			response = self.httpapi.delete(uri, params, data)
			return response
		except Errors.svtError as e:
			print("Error: ", e.code, e.msg, e.call)
			raise

		
	