# this python file uses the following encoding: utf-8
import logging
import os
import json
import re


# defaults
SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'
SQLALCHEMY_ECHO = False
LOG_LEVEL = 'DEBUG'


# check config.json
if os.path.isfile('config.json'):
    with open('config.json') as inf:
        config = json.load(inf)
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)
    LOG_LEVEL = config.get('LOG_LEVEL', LOG_LEVEL)


# check env
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)
LOG_LEVEL = os.environ.get('LOG_LEVEL', LOG_LEVEL)


# set logging
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s:%(lineno)d %(message)s',
    datefmt='%Y%m%d-%H%M%S',
    level=dict(debug=logging.DEBUG, warning=logging.WARNING, info=logging.INFO).get(LOG_LEVEL.lower()))
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


# some initial logs
log = logging.getLogger(__name__)
show_db_uri = SQLALCHEMY_DATABASE_URI
if len(re.findall(r'^(\w+://.+?)(:.*@)(.+)$', show_db_uri)) > 0:
    show_db_uri = re.sub(r'^(\w+://.+?)(:.*@)(.+)$', r'\1:*****@\3', show_db_uri)

log.info('LOG_LEVEL: %s' % LOG_LEVEL)
log.info('SQLALCHEMY_DATABASE_URI: %s' % show_db_uri)
