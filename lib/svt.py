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
	def hook_marker(self, d):
		selector = self.selector
		marker = self.marker
		# Outer nest json has 'svt_cdb_key', enforced by CouchDB views 
		if not 'svt_cdb_key' in d:
			return(d)
		# Get the selected subjson
		s = d['svt_cdb_value'][selector]
		# Is it a dict ? 
		if isinstance(s,dict):
			v = s[marker]
		# Is it a list ?
		# Each item has been keyed with 'svt_unic' by the view
		elif not isinstance(s, basestring):
			v = {}
			for i in s:
				svt_unic = i['svt_unic']
				# Get the marked value
				if marker in i['svt_value']:
					marked = i['svt_value'][marker]
				# Marker not found
				else:
					marked = 'svt_no_data'
				# Gracefully manage errors in map
				if svt_unic not in v:
					v[svt_unic] =  marked
					v['svt_marked'] = True
				else:
					raise('Map function for selector: ' + selector + ' keys with non unique key')
		else:
			raise('Guru meditation, call the developper!')
		# Add the key to the result
		(collect, client, source, name) = d['svt_cdb_key']
		r = {
				'collect':collect,
				'client':client,
				'source':source,
				'name':name,
				'value':v
			}
		return Svt(**r)

	# Used for json.loads object_hook 
	# Get all first level markers
	def hook_all(self, d):
		selector = self.selector
		# Outer nest json has 'svt_cdb_key', enforced by CouchDB views 
		if not 'svt_cdb_key' in d:
			return(d)
		# Get the selected subjson
		s = d['svt_cdb_value'][selector]
		# Is it a dict ? 
		if isinstance(s,dict):
			v = s 
		# Is it a list ?
		# Each item has been keyed with 'svt_unic' by the view
		elif not isinstance(s, basestring):
			v = {}
			for i in s:
				svt_unic = i['svt_unic']
				marked = i['svt_value']
				# Gracefully manage errors in map
				if svt_unic not in v:
					v[svt_unic] =  marked
					v['svt_marked'] = True
				else:
					raise('Map function for selector: ' + selector + ' keys with non unique key')
		else:
			raise('Guru meditation, call the developper!')
		# Add the key to the result
		(collect, client, source, name) = d['svt_cdb_key']
		r = {
				'collect':collect,
				'client':client,
				'source':source,
				'name':name,
				'value':v
			}
		return Svt(**r)
