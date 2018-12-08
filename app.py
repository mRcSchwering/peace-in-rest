from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
import json

# TODO: scaling with swagger
# https://flask-restplus.readthedocs.io/en/latest/scaling.html
# and
# http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

# TODO: ssl
# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

# TODO: token-based
# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask

config_file = 'config.json'


# Setup
app = Flask(__name__)
api = Api(app, version='1.0', title='PIR')
log = app.logger
parser = reqparse.RequestParser()
auth = HTTPBasicAuth()
ns = api.namespace('api', description='description for mirror')

with open(config_file) as inf:
    config = json.load(inf)

app.secret_key = config['flaskSecretKey']
data = config['data']


@auth.verify_password
def verify_password(username, password):
    for account in config['accounts']:
        if account['user'] == username:
            if account['password'] == password:
                return True
    return False


# Endpoints
@ns.route('/data')
class Data(Resource):
    '''Look at all records'''

    @auth.login_required
    def get(self):
        '''Get all records'''
        return data


@ns.route('/data/<string:name>')
class Record(Resource):
    '''Look at specific records'''

    @auth.login_required
    def get(self, name):
        '''Get record by name'''
        return [d for d in data if d['name'] == name]


@ns.route('/mirror')
class Mirror(Resource):
    '''Nonsense endpoint'''

    @auth.login_required
    def post(self):
        '''Return whatever you posted as shoutout'''
        parser.add_argument('shoutout', type=str, help='Some message')
        args = parser.parse_args(strict=True)
        return args


#api.add_resource(Data, '/data', '/', endpoint='data')
#api.add_resource(Record, '/data/<string:name>', '/', endpoint='record')
#api.add_resource(Mirror, '/mirror', '/', endpoint='mirror')
