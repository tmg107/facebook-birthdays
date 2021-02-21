from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


## intiate classes and relationships between classes
class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(150))
    birthday = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    birthday = db.relationship('Birthday')
























