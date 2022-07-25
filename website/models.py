"""All the DB infomation"""
from lib2to3.pgen2.token import STRING
import string
from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db


# database model for notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    about = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# database model for books
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    author = db.Column(db.String(150))
    rating = db.Column(db.Integer)
    imageLink = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# database model for users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    books = db.relationship('Book')
    notes = db.relationship('Note')
