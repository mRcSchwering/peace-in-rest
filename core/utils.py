# this python file uses the following encoding: utf-8
from flask_httpauth import HTTPBasicAuth
import json
from data import conn as db


class Utils(object):

    config_file = 'config.json'

    def __init__(self):
        with open(self.config_file) as inf:
            self.config = json.load(inf)
        self.data = self.config['data']
        self.flask_secret_key = self.config['flaskSecretKey']
        self._setUp_auth()

    def _setUp_auth(self):
        auth = HTTPBasicAuth()

        @auth.verify_password
        def verify_password(username, password):
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            return db.is_login_valid(username, password)

        self.auth = auth
