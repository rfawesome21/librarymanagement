from __init__ import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


""" enrollment = db.Table('enrollment',db.Model.metadata,
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id',db.Integer, db.ForeignKey('book.id'))
) """

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200),index = True)
    last_name = db.Column(db.String(200),index = True)
    username = db.Column(db.String(200), index = True)
    email = db.Column(db.String(200), index = True)
    password = db.Column(db.String(200),index = True)
    year = db.Column(db.Date)
    #book = db.relationship('Book', secondary = enrollment)
    #def __repr__(self):
    #   return f"User('{self.firstname}', '{self.lastname}', '{self.username}','{self.password}','{self.email}','{self.year}')"
    def __init__(self,first_name,last_name,email,user_name, year):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = user_name
        self.year = year

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
""" class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),index = True)
    author = db.Column(db.String(200),index = True)
    genre = db.Column(db.String(200),index = True)
    user = db.relationship('User', secondary = enrollment)
    #book_adder = db.Column(db.String(200), db.ForeignKey('admin.username'))
    def __repr__(self):
        return self.name + ' ' + self.author + ' ' + self.genre
 """""" 
class Admin(db.Model):
    username = db.Column(db.String(200),primary_key = True)
    password = db.Column(db.String(200),index = True)
    authenticated = db.Column(db.Boolean, default = False)
    book = db.relationship('Book',backref = 'admin', lazy = 'dynamic')
    def is_active(self):
        return True
    def is_authenticated(self):
        return self.is_authenticated """
