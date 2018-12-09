# this python file uses the following encoding: utf-8
from flask import Flask
from apis import api
from core.utils import Utils

# TODO fields, objects benutzen - e.g. User object

# TODO sqlite database mit usern
# TODO reset db via REST call

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
