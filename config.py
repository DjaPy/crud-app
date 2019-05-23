import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

SECRET_KEY_DEFAULT = 'test_app_one'
SECRET_KEY = os.environ.get("SECRET_KEY", default=SECRET_KEY_DEFAULT)

TYPE_DB = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_NAME = 'db_users'

db_connect = '{0}+{1}://{2}@{3}/{4}'.format(
    TYPE_DB, DB_DRIVER, DB_USER, DB_HOST, DB_NAME,
)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_connect
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(app)

ma = Marshmallow(app)

login = LoginManager(app)

