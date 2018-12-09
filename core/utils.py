# this python file uses the following encoding: utf-8
from flask_httpauth import HTTPBasicAuth
import json


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
            for account in self.config['accounts']:
                if account['user'] == username:
                    if account['password'] == password:
                        return True
            return False

        self.auth = auth
