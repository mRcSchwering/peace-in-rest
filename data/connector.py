# this python file uses the following encoding: utf-8
from .models import User


class Connector(object):

    def __init__(self, session):
        self.session = session

    def fill_with_test_data(self):
        self.session.add_all([
            User(name='u1', password='u1'),
            User(name='u2', password='u2')
        ])
        self.session.commit()

    def is_login_valid(self, user, password):
        for u, p in self.session.query(User.name, User.password):
            if user == u:
                if password == p:
                    return True
        return False
