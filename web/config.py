import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

DEBUG = os.environ.get('DEBUG', default=True)

SECRET_KEY_DEFAULT = 'test_app_one'
SECRET_KEY = os.environ.get("SECRET_KEY", default=SECRET_KEY_DEFAULT)

TYPE_DB = os.environ.get('TYPE_DB', default='postgresql')
DB_DRIVER = os.environ.get('DB_DRIVER', default='psycopg2')
DB_USER = os.environ.get('DB_USER', default='postgres')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST', default='localhost')
DB_PORT = os.environ.get('DB_PORT', default=5432)
DB_NAME = os.environ.get('DB_NAME', default='db_users')

db_connect = '{0}+{1}://{2}:{3}@{4}:{5}/{6}'.format(
    TYPE_DB, DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME,
)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_connect
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = DEBUG
app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(app)

ma = Marshmallow(app)

login = LoginManager(app)

