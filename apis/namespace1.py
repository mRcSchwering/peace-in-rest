# this python file uses the following encoding: utf-8
from flask_restplus import Namespace, Resource, reqparse
from core.utils import Utils

api = Namespace('records', description='records related operations')
utils = Utils()
auth = utils.auth


@api.route('/')
class AllRecords(Resource):
    '''Look at all records'''

    @auth.login_required
    def get(self):
        '''Get all records'''
        return utils.data


@api.route('/<string:name>')
class Record(Resource):
    '''Look at specific records'''

    @auth.login_required
    def get(self, name):
        '''Get record by name'''
        return [d for d in utils.data if d['name'] == name]
