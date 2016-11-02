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


class Svt:

	def __init__(self, **kw):
		self.__dict__.update(kw)	


	# Used for json.loads object_hook
	def hook(self, d):
		selector = self.selector
		marker = self.marker
		# Outer nest json has 'key', enforced by CouchDB views 
		if not 'key' in d:
			return(d)
		# Get the selected subjson
		s = d['value'][selector]
		# Is it a dict ? 
		if isinstance(s,dict):
			v = s[marker]
		# Is it a list ?
		# Each item has been dictionarized by the view
		elif not isinstance(s, basestring):
			v = {}
			for i in s:
				svt_unic = i['svt_unic']
				marked = i['svt_value'][marker]
				v[svt_unic] =  marked
				v['svt_marked'] = True
		else:
			raise('Guru meditation, call the developper!')
		# Add the key to the result
		(collect, client, source, name) = d['key']
		r = {
				'collect':collect,
				'client':client,
				'source':source,
				'name':name,
				'value':v
			}
		return Svt(**r)


