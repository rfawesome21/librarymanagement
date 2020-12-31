from __init__ import db, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin
from forms import RegisterUser, LoginForm

roles_user = db.Table('user_roles',db.Model.metadata,
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id'))
) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200),index = True)
    last_name = db.Column(db.String(200),index = True)
    username = db.Column(db.String(200), index = True)
    email = db.Column(db.String(200), index = True)
    password = db.Column(db.String(200),index = True)
    year = db.Column(db.Date)
    roles = db.relationship('Role',secondary = roles_user, backref = 'users' , lazy = 'dynamic')
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    #book = db.relationship('Book', secondary = enrollment)
    #def __repr__(self):
    #   return f"User('{self.firstname}', '{self.lastname}', '{self.username}','{self.password}','{self.email}','{self.year}')"
    def __init__(self, first_name, last_name, username, password, email, year, roles, active):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.year = year
        self.roles = roles
        self.active = active

class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),index = True)
    description = db.Column(db.String(250), index = True)

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),index = True)
    author = db.Column(db.String(200),index = True)
    genre = db.Column(db.String(200),index = True)
    #user = db.relationship('User', secondary = enrollment)
    #book_adder = db.Column(db.String(200), db.ForeignKey('admin.username'))
    def __init__(self,name,author,genre):
        self.name = name
        self.author = author
        self.genre = genre

db.create_all()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form = RegisterUser)

