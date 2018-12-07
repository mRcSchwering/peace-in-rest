from flask import Flask, session, redirect, url_for, escape, request, jsonify
import json

config_file = 'config.json'


# Setup
with open(config_file) as inf:
    config = json.load(inf)

app = Flask(__name__)
log = app.logger
app.secret_key = config['flaskSecretKey']
data = config['data']


# Pages
def login_page(error):
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
        <div style="color: red">%s</div>
    ''' % error


def index_page(user):
    return 'Logged in as %s' % escape(user)


# Misc
def login_is_valid(user, password):
    accounts = [a for a in config['accounts'] if a['user'] == user]
    if len(accounts) is not 1:
        return False
    if accounts[0]['password'] != password:
        return False
    return True


# Actions
def log_user_in():
    session['username'] = request.form['username']
    return redirect(url_for('index'))


def log_user_out():
    session.pop('username', '')
    return redirect(url_for('login'))


# Endpoints
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return index_page(session['username'])


@app.route('/data')
def get_all_data():
    if 'username' not in session:
        return redirect(url_for('login'))
    return jsonify(data)


@app.route('/data/<string:name>')
def get_data_for_record(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    return jsonify([d for d in data if d['name'] == name])


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('login'))
    log.debug('Logout - user: %s - successful' % session['username'])
    return log_user_out()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if login_is_valid(user, password):
            log.debug('Login - user: %s - successful' % user)
            return log_user_in()
        else:
            log.debug('Login - user: %s - failed' % user)
            error = 'Invalid username/password'
    return login_page(error)
