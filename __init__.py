from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
import os
#creates a database from sqlalchemy
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = False
app.config['SECURITY_PASSWORD_SALT'] = "sha256"
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SESSION_TYPE'] = "sqlalchemy"
app.config['SESSION_SQLALCHEMY'] = db

secret_key = os.urandom(24)
mail = Mail(app)
app.secret_key=secret_key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app, name='microblog', template_mode='bootstrap3')
Migrate = Migrate(db,app)
manager = Manager(app)
sess = Session(app)

manager.add_command('db', MigrateCommand)
