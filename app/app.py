# This software may contain the intellectual property of EMC Corporation or be
# licensed to EMC Corporation from third parties. Use of this software and the
# intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on behalf
# of EMC. This code is provided AS IS, without warranty of any kind express or
# implied.

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"


import cfg.config
from lib.wrapper import Wrapper
from lib.errors import Errors
from flask import Flask
from flask_restplus import Resource, Api



app = Flask(__name__)
api = Api(app, default='svt_couchdb', default_label='svt_couchdb')

settings = cfg.config.NORMAL_SETTINGS

@api.route('/list', methods=['GET'])
class list(Resource):
	def get(self):
		res = Wrapper().lister(settings)
		return res

if __name__ == '__main__':
	app.run(debug=True)
