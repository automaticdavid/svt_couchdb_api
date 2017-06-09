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
from lib.errors import Errors
from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse
from werkzeug import secure_filename, FileStorage


__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"

settings = cfg.config.NORMAL_SETTINGS
yamldefs = cfg.config.YAML_DEFS

app = Flask(__name__)
api = Api(app)
ns = api.namespace('api', description='API access to couchdb queries')


''' Upload parser '''


parser = reqparse.RequestParser()
upload_parser = ns.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type=FileStorage,
    required=True
)
upload_parser.add_argument('client', required=True)


''' Model definitions '''


m_upload = ns.model('M_upload', {
    'client': fields.String(description='Name of the client', example='Test1'),
    'file': fields.String(
        description='File name',
        example='/home/zen/work/output_svt_2016-09-12-11-45-45.zip')
    })

m_delete = ns.model('M_delete', {
    'client': fields.String(description='Name of the client', example='Test1'),
    'date': fields.String(
        description='Date of Collect',
        example='2016-09-12-11-45-45')
    })

m_generate = ns.model('M_generate', {
    'client': fields.String(description='Name of the client', example='Test1'),
    'date': fields.String(
        description='Date of Collect',
        example='2016-09-12-11-45-45'),
    'yamldef': fields.String(
        description='Type of report',
        example='/home/zen/work/vro-plugins.yaml'),
    })

m_extract = ns.model('M_generate', {
    'client': fields.String(description='Name of the client', example='Test1'),
    'date': fields.String(
        description='Date of Collect',
        example='2016-09-12-11-45-45'),
    })


''' Error handler '''


@api.errorhandler(Errors.genError)
def handleError(error):
    '''Return a custom message and 400 status code'''
    return {'message': error.msg}, 500


''' Routes '''


@ns.route('/list', methods=['GET'])
class list(Resource):
    def get(self):
        res = Wrapper().lister(settings)
        return res


@ns.route('/upload', methods=['POST'])
class upload(Resource):

    # @ns.expect(m_upload)
    @ns.expect(upload_parser)
    def post(self):
        file = request.files['file']
        args = upload_parser.parse_args()
        client = args['client']
        res = Wrapper().loader(settings, file, client)
        return res


@ns.route('/delete', methods=['POST'])
class delete(Resource):

    @ns.expect(m_delete)
    def post(self):
        date = request.json['date']
        client = request.json['client']
        res = Wrapper().deleter(settings, date, client)
        return res


@ns.route('/generate', methods=['POST'])
class generate(Resource):

    @ns.expect(m_generate)
    def post(self):
        date = request.json['date']
        client = request.json['client']
        yamldef = request.json['yamldef']
        res = Wrapper().generator(settings, date, client, yamldef)
        return res


@ns.route('/extract/<string:ddoc>/<string:view>', methods=['POST'])
@ns.doc(params={'ddoc': 'Name of the ddoc', 'view': 'Name of the View'})
class extract(Resource):

    @ns.expect(m_extract)
    def post(self, ddoc, view):

        yamldef = yamldefs + '/' + ddoc + '_' + view + ".yaml"
        date = request.json['date']
        client = request.json['client']
        res = Wrapper().generator(settings, date, client, yamldef)
        return res


if __name__ == '__main__':
    app.run(debug=True)
