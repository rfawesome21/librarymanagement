from __init__ import db, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin
from forms import RegisterUser, LoginForm
from datetime import datetime

roles_user = db.Table('user_roles',db.Model.metadata,
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id')),
    db.UniqueConstraint('user_id','role_id', name = 'UC_user_id_role_id')
) 

book_user = db.Table('book_users',db.Model.metadata,
    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id',db.Integer, db.ForeignKey('book.id')),
    db.UniqueConstraint('user_id','book_id',name='UC_user_id_book_id')
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200),index = True)
    last_name = db.Column(db.String(200),index = True)
    username = db.Column(db.String(200), index = True)
    email = db.Column(db.String(200), index = True)
    password = db.Column(db.String(200),index = True)
    year = db.Column(db.Date)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role',secondary = roles_user, backref = 'users')
    book = db.relationship('Book', secondary = book_user, lazy = 'select')

    def leave_book(self,book):
        self.book.remove(book)

class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),index = True)
    description = db.Column(db.String(250), index = True)

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),index = True)
    author = db.Column(db.String(200),index = True)
    genre = db.Column(db.String(200),index = True)
    synopsis = db.Column(db.String(20000), index = True)
    userNumber = db.Column(db.Integer, index = True)
    user = db.relationship('User', secondary = book_user, lazy = 'select')
    date_borrowed = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,name,author,genre):
        self.name = name
        self.author = author
        self.genre = genre

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form = RegisterUser)
user_datastore.find_or_create_role(name='end-user', description='End user')
user_datastore.find_or_create_role(name='admin', description='Administrator')

db.create_all()

