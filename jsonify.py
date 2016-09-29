# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

__author__ = "David CLAUVEL"
__version__ = "0.1"
__status__ = "Concept Code"

import os
from collections import OrderedDict
from xmljson import BadgerFish
from xml.etree.ElementTree import fromstring
import simplejson as json

bf = BadgerFish(dict_type=OrderedDict)  

source = '/home/zen/work/2/src/nsx-1/'
target = '/home/zen/work/2/tgt/nsx-1/'
collect = '20160101120015'

for src in os.listdir(source):
	if src.endswith('.json'):
		# Open source json file
		fi = open (source + src, 'r')
		s = fi.read()
		print('Converting: ', src)
		# Call BadgerFish conversion
		b = bf.data(fromstring(s))
		# Add source info
		filename = os.path.splitext(src)[0]
		sourcedir = os.path.basename(os.path.dirname(source))
		info = {'ehc_source_file':filename, 'ehc_source_dir':sourcedir, 'ehc_collect_date':collect}
		b.update(info)
		# Write json file
		tgt = target + os.path.basename(src) + '.json'
		fo = open (tgt, 'w')
		j = json.dump(b, fo)



