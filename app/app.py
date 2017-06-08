"""
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
"""

import cfg.config
from lib.wrapper import Wrapper
from flask import Flask, request
from flask_restplus import Resource, Api, fields


__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"

settings = cfg.config.NORMAL_SETTINGS
yamldefs = cfg.config.YAML_DEFS

app = Flask(__name__)
api = Api(app)
ns = api.namespace('api', description='API access to couchdb queries')


@ns.route('/list', methods=['GET'])
class list(Resource):
    def get(self):
        res = Wrapper().lister(settings)
        return res


@ns.route('/upload', methods=['POST'])
class upload(Resource):

    fields = api.model('Resource', {
        'file': fields.String,
        'client': fields.String
    })

    @ns.expect(fields)
    def post(self):
        f = request.json['file']
        client = request.json['client']
        res = Wrapper().loader(settings, f, client)
        return res


@ns.route('/delete', methods=['POST'])
class delete(Resource):

    fields = api.model('Resource', {
        'file': fields.String,
        'date': fields.String,
    })

    @ns.expect(fields)
    def post(self):
        date = request.json['date']
        client = request.json['client']
        res = Wrapper().deleter(settings, date, client)
        return res


@ns.route('/generate', methods=['POST'])
class generate(Resource):

    fields = api.model('Resource', {
        'date': fields.String,
        'client': fields.String,
        'yamldef': fields.String,
    })

    @ns.expect(fields)
    def post(self):
        date = request.json['date']
        client = request.json['client']
        yamldef = request.json['yamldef']
        res = Wrapper().generator(settings, date, client, yamldef)
        return res


@ns.route('/extract/<string:ddoc>/<string:view>', methods=['POST'])
class extract(Resource):

    fields = api.model('Resource', {
        'date': fields.String,
        'client': fields.String
    })

    @ns.expect(fields)
    def post(self, ddoc, view):

        yamldef = yamldefs + '/' + ddoc + '_' + view + ".yaml"
        date = request.json['date']
        client = request.json['client']
        res = Wrapper().generator(settings, date, client, yamldef)
        return res


if __name__ == '__main__':
    app.run(debug=True)
