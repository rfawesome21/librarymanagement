from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#creates a database from sqlalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key='12345'
db = SQLAlchemy(app)
