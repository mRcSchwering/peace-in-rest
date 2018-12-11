# this python file uses the following encoding: utf-8
from flask import Flask
from apis import api
from core.utils import Utils
from data import conn as db

# TODO fields, objects benutzen - e.g. User object

# TODO users zum laufen kriegen
# vllt darf ich in dem Fall keine Klasse nehmen (connector.py)
# modules sind singletons -> wäre hier vllt besser
# auch mal log debuggen, wie häufig eigentlich instanziiert wird

# TODO n paar daten mit 2 tables und foreign keys

# full example:
# http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

# TODO: ssl
# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

# TODO: token-based
# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask


utils = Utils()
app = Flask(__name__)
app.secret_key = utils.flask_secret_key
api.init_app(app)
app.run(debug=True)
db.fill_with_test_data()
