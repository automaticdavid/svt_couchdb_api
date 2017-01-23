# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.


__author__ = "David CLAUVEL"
__version__ = "v0.1"
__status__ = "Concept Code"


class Errors(Exception):

	class svtError(Exception):
		
		def __init__(self, r, url):

			self.code = r.status_code
			self.msg = r.text
			self.call = r.url
			self.debug = []

	class genError(Exception):

		def __init__(self, code, msg, call, debug):

			self.code = code
			self.msg = msg
			self.call = call
			self.debug = debug
		

	class reqError(Exception):

		def __init__(self, url, debug):

			self.call = url
			self.debug = debug