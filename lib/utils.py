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
from zipfile import ZipFile
import simplejson as json
import sys
import os
import collections
from lib.errors import Errors

# Module level logger
logger = logging.getLogger(__name__)
	
class Utils:

	# Autovivifying hash structure
	def hash(self):
		return collections.defaultdict(Utils().hash)

	# Extract files in memory from zip
	def extractor(self, f):
		r = []
		inputzip = ZipFile(f)
		for name in inputzip.namelist():
			content = inputzip.read(name)
			r.append((name, content))
		return(r)

	# Decorate collected JSONs
	def decorator(self, f, client):
		result = {}
		# Extract collect from zip filename
		fullname = os.path.basename(f)
		name = os.path.splitext(fullname)[0]
		collect = name.replace('output_svt_','')
		# In memory zip extract
		rows = Utils().extractor(f)
		for row in rows:
			name = row[0]
			content = row[1]
			if name.endswith('.json') and content:
				# extract information from path
				path = name.split('/')
				source = path[1]
				filename = path[2]
				info = {'svt_source_file':filename, 
						'svt_source':source, 
						'svt_collect_date':collect, 
						'svt_client':client}	
				# add information to the json
				try:	
					j =json.loads(content)
					j.update(info)
					result[name] = json.dumps(j)
				except:
					print("Invalid JSON for json.loads in file: " + name)
					pass
		return(result)

	# Follow links in a vipr json
	def expander(self, j, viprsource, links):
		e = {}
		if isinstance(j,dict):
			for k,v in j.iteritems():
				# First level link
				if k == 'link' and 'href' in v:
					href = v['href']
					urn = os.path.basename(href)
					# Lookup the linked json in the links dict
					if urn in links[viprsource]:
						link = links[viprsource][urn]
						# Remove self link if needed
						if 'link' in link:
							link.pop('link')
					else:
						link = {'SVT_LINK_NOT_FOUND':'SVT_LINK_NOT_FOUND'}
					e.update(link)
				# A sub json may contain links
				elif isinstance(v,dict):
					e[k] = Utils().expander(v, viprsource, links)
				# A value may be a list of links
				elif isinstance(v,list):
					l = []
					for it in v:
						r = Utils().expander(it, viprsource, links)
						l.append(r)
					e[k] = l
				# A string value may be a urn without a link key
				elif k != 'id' and isinstance(v,basestring) and v.startswith('urn:'):
					if links[viprsource][v]:
						e[k] = links[viprsource][v]
					else:
						e[k] = 'SVT_LINK_NOT_FOUND'
					e[k] = v
		# Standalone strings might also be links
		else:
			if j != 'id' and isinstance(j,basestring) and j.startswith('urn:'):
				if j in links[viprsource]:
					e = links[viprsource][j]
				else:
					e = 'SVT_LINK_NOT_FOUND'
			else:	
				e = j
		return(e)

	# Transform the YAML def of a report
	# Return a dict with the markers as a list value of the couch call
	def flatten(self, d):
		ddocs = d['reports']
		result = {}
		for ddoc in ddocs:
			selectors = ddocs[ddoc]
			for selector in selectors:
				markers = selectors[selector]
				for marker in markers:
					if (ddoc, selector) in result:
						result[(ddoc, selector)].append(marker)
					else: 
						result[(ddoc, selector)] = [marker]
		return(result)

	# Replace the default keys in a CouchDB response
	# Use cutom keys that won't yield hook errors
	def cleanKeys(self, r):
			j = json.loads(r)
			r = []
			for row in j['rows']:
				svt_cdb_value = row['value']
				svt_cdb_key = row['key']
				cdb_row = {'svt_cdb_key': svt_cdb_key, 'svt_cdb_value': svt_cdb_value}
				r.append(cdb_row)
			d = json.dumps(r)
			return(d)

	# Enrich a dictionary with the result rows of a view
	def jsonify(self, res, caller, rows):

		ddoc = caller[2]
		selector = caller[3]
		marker = caller[4]

		for row in rows:

			# Get values from the row object
			collect = row.collect
			client = row.client
			source = row.source
			name = row.name
			value = row.value
			action = row.action

			# print("DEBUG -  marker:{}, action:{}, name:{}, value:{}, typevalue:{}".format(marker, action, name, value, type(value))) 

			# Keep collect and date in the result and sanity check them
			if not 'info' in res:
				res['info']['svt_collect'] = collect
				res['info']['svt_client'] = client
			elif (res['info']['svt_collect'] != collect 
				and res['info']['svt_client'] != client):
				code = 99
				msg = "Different keys found in Generator" 
				call = (res, caller, row)
				debug = "" 
				raise Errors.genError(code, msg, call, debug)

			
			#########################################################################################
			# multi
			#########################################################################################

			if ( action == 'svt_multi' 
				and marker == 'svt_all'
				and isinstance(value,dict)):
				# Getting svt_all instead of specific marker
				# Need to clean output from using multifile based name
				# Multiple file values are keyed by name
				# print("DEBUG: GENTYPE : multi, all, dict" )
				try:
					del value['svt_collect_date']
					del value['svt_client']
					del value['svt_source']
					del value['svt_source_file']
					del value['_id']
					del value['_rev']
				except KeyError:
					pass
				for k in value.keys():
					if k != 'svt_marked':
						res['data'][source][ddoc][selector][name][k] = value[k]

			elif (action == 'svt_multi'
				and marker == 'svt_all'):
				# multi and all for non dict value
				# Multiple file values are keyed by name
				# print("DEBUG: GENTYPE: multi, all, non dict" )
				res['data'][source][ddoc][selector][name] = value
			
			elif (action == 'svt_multi'): 
				# multi and marker for non dict value
				# Multiple file values are keyed by name
				# Need to filter svt_no_data from other files
				# Sanity check for duplicate markers across files
				# print("DEBUG: GENTYPE: multi, marker, non dict" )
				leaf = res['data'][source][ddoc][selector][name]
				if marker not in leaf:
					res['data'][source][ddoc][selector][name][marker] = value
				elif value != 'svt_no_data' and leaf[marker] == 'svt_no_data':
					res['data'][source][ddoc][selector][name][marker] = value
				elif (leaf[marker] != 'svt_no_data'
					and value != 'svt_no_data'
					and value != leaf[marker]):
					raise Exception("ERROR: duplicate value for marker: " + marker)

			#########################################################################################
			# group
			#########################################################################################

			elif (action == 'svt_group'
				and marker == 'svt_all'
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# Marked values are to be re-keyed
				# Remove the marked tag
				del value['svt_marked']
				for k in value.keys():
					res['data'][source][ddoc][selector][name][k]  = value[k]

			elif (action == 'svt_group'
				and marker == 'svt_all'
				and isinstance(value,dict)):
				# Need to clean output from using multifile based values
				# using name instead of selector 
				try:
					del value[name]['svt_collect_date']
					del value[name]['svt_client']
					del value[name]['svt_source']
					del value[name]['svt_source_file']
					del value[name]['_id']
					del value[name]['_rev']
				except KeyError:
					pass
				res['data'][source][ddoc][selector][name] = value[name]
				
			elif (action == 'svt_group'
				and marker == 'svt_all'):
				res['data'][source][ddoc][selector][name] = value

			elif (action == 'svt_group'
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# Marked values are to be re-keyed
				# Remove the marked tag
				del value['svt_marked']
				for k in value:
					res['data'][source][ddoc][selector][name][k]  = value[k]

			elif (action == 'svt_group'
				and marker == name): 
				try:
					del value['svt_collect_date']
					del value['svt_client']
					del value['svt_source']
					del value['svt_source_file']
					del value['_id']
					del value['_rev']
				except KeyError:
					pass
				res['data'][source][ddoc][selector][name] = value


			#########################################################################################
			# single
			#########################################################################################

			elif (action == 'svt_single'
				and marker == 'svt_all'
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# Getting single file values
				# Getting svt_all instead of specific marker
				# Marked values are to be re-keyed
				# Remove the marked tag
				# print("DEBUG: GENTYPE: single, all, marked, dict" )
				leaf = res['data'][source][ddoc][name]
				del value['svt_marked']
				for k in value.keys():
					res['data'][source][ddoc][selector][k]  = value[k]
	
			elif (action == 'svt_single'
				and marker == 'svt_all'):
				# print("DEBUG: GENTYPE: single, all" )
				# Getting svt_all for single file values
				# Attach them all at the selector level
				# Need to clean output from using the whole json
				try:
					del value['svt_collect_date']
					del value['svt_client']
					del value['svt_source']
					del value['svt_source_file']
					del value['_id']
					del value['_rev']
				except KeyError:
					pass
				res['data'][source][ddoc][selector].update(value)

			elif (action == 'svt_single'
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# print("DEBUG: GENTYPE: single, marked, dict" )
				# Getting single files values for marker
				# Marked values are to be re-keyed
				# Remove the marked tag
				del value['svt_marked']
				for k in value.keys():
					res['data'][source][ddoc][selector][k][marker]  = value[k]

			elif action == 'svt_single':
				# print("DEBUG: GENTYPE: single, marker" )
				# Getting single file value for a specific marker
				# Using marker won't select doc level info
				res['data'][source][ddoc][selector][marker] = value

			#########################################################################################
			# standard
			#########################################################################################

			elif (action == 'svt_standard'
				and marker == 'svt_all' 
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# Getting svt_all instead of specific marker
				# Marked values are to be re-keyed
				# Remove the marked tag
				del value['svt_marked']
				for k in value.keys():
					res['data'][source][ddoc][name][selector][k]  = value[k]
			
			elif (action == 'svt_standard'
				and marker == 'svt_all'):
				# Getting svt_all for ungrouped value
				# Attach them all under their name
				res['data'][source][ddoc][name][selector].update(value)

			elif (action == 'svt_standard'
				and isinstance(value,dict) 
				and 'svt_marked' in value):
				# Getting specific marker
				# Marked values are to be re-keyed
				# Remove the marked tag
				del value['svt_marked']
				for k in value.keys():
					res['data'][source][ddoc][name][selector][k][marker] = value[k]

			elif action == 'svt_standard':
				# Standard attach 
				res['data'][source][ddoc][name][selector][marker] = value

			# else:
			# 	raise Exception("Error: Got unkown action: " + action + " from map: " + ddoc + '/' + selector)

		return(res)


