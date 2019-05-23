import datetime

from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_login import UserMixin
from config import db, ma, login


class Admin(UserMixin, db.Model):
    __table_name__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow
    )
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password_hash = generate_password_hash(
            password, salt_length=8
        )

    def __repr__(self):
        return '<Admin {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))


class Person(db.Model):
    __table_name__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String)
    fname = db.Column(db.String)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    age = db.Column(db.Integer)
    job = db.Column(db.String)

    def __repr__(self):
        return '<{0} {1}>'.format(self.fname, self.lname)


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = Person
        sqla_session = db.session
