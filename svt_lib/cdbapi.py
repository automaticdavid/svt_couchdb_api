'''
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
'''

import logging
from svt_lib.httpapi import HTTPApi
from svt_lib.errors import Errors

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"

# module level logger
logger = logging.getLogger(__name__)


class CouchResponse:

    def __init__(self, config):
        self.httpapi = HTTPApi(
            config.host, config.protocol, config.port,
            config.username, config.password, config.debug,
            config.db, config.verify)

    def get(self, uri, cookie):
        logger.debug('URI : %s', uri)
        try:
            response = self.httpapi.get(uri, cookie)
            return response
        except Errors.svtError as e:
            # print("Error: ", e.code, e.msg, e.call)
            raise

    def put(self, uri, cookie, params=None, data=None):
        logger.debug('URI : %s', uri)
        try:
            response = self.httpapi.put(uri, cookie, params, data)
            return response
        except Errors.svtError as e:
            # print("Error: ", e.code, e.msg, e.call)
            raise

    def delete(self, uri, cookie, params=None, data=None):
        logger.debug('URI : %s', uri)
        try:
            response = self.httpapi.delete(uri, cookie, params, data)
            return response
        except Errors.svtError as e:
            # print("Error: ", e.code, e.msg, e.call)
            raise

    def post(self, uri, cookie, params=None, data=None):
        logger.debug('URI : %s', uri)
        try:
            response = self.httpapi.post(uri, cookie, params, data)
            return response
        except Errors.svtError as e:
            # print("Error: ", e.code, e.msg, e.call)
            raise

    def getCookie(self):
        try:
            uri = '/_session'
            data = {
                'name': self.httpapi.username,
                'password': self.httpapi.password}
            logger.debug('URI : %s', uri)
            response = self.httpapi.post(uri, 'getCookie', None, data)
            return(response)
        except Errors.svtError as e:
            # print("Error: ", e.code, e.msg, e.call)
            raise
