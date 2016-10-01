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



# Module level logger
logger = logging.getLogger(__name__)
	
class Utils:

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
		rows = Utils().extractor(f)
		for row in rows:
			name = row[0]
			content = row[1]
			if name.endswith('.json') and content:
				# extract information from path
				path = name.split('/')
				collect = path[0].replace('output_svt_','')
				source = path[1]
				filename = path[2]
				info = {'svt_source_file':filename, 'svt_source':source, 'svt_collect_date':collect, 'svt_client':client}	
				# add information to the json
				try:	
					j =json.loads(content)
					j.update(info)
					result[name] = json.dumps(j)
				except AttributeError as err:
					print("Invalid JSON for json.loads in file: " + name)
					pass
		return(result)

	# Follow links in a vipr json
	def expander(self, j, viprsource, links):
		e = {}
		print("boo")
		print(j)
		print("####")
		if isinstance(j,dict):
			for k,v in j.iteritems():
				print("===> " + k )
				if k == 'id':
					if 'urn' in j['id']:
						urn = j['id']
						if urn in links[viprsource]:
							link = links[viprsource][urn]
						else:
							link = "NOT FOUND"
						e['id_tracker'] = urn
						e['value'] = link
				elif isinstance(v,dict):
					print("TTT")
					print(v)
					e[k] = Utils().expander(v, viprsource, links)
				else:
					e[k] = v
		else:
			e = j
		return(e)


	# Transform the YAML def of a report
	# Return a LoL with the elements needed by couch calls 
	def flatten(self, d):
		client = d['client']
		collect = d['collect']
		reports = d['reports']
		result = []
		for report in reports:
			sources = reports[report]
			for source in sources:
				selectors = sources[source]
				for selector in selectors:
					result.append([[client, collect, report], [source, selector]])
		return(result)

	# Transform result structures into tables
	def tableizer(self, caller, struct):
		print('=' * 80)
		print(caller)
		print(struct.key)
		print(struct.value)



