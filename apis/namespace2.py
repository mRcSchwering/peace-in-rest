# this python file uses the following encoding: utf-8
from flask_restplus import Namespace, Resource, reqparse
from core.utils import Utils

api = Namespace('mirror', description='just something with a POST')
parser = reqparse.RequestParser()
utils = Utils()
auth = utils.auth


@api.route('/')
class Mirror(Resource):
    '''Nonsense endpoint'''

    @auth.login_required
    def post(self):
        '''Return whatever you posted as shoutout'''
        parser.add_argument('shoutout', type=str, help='Some message')
        args = parser.parse_args(strict=True)
        return args
