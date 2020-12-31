from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectMultipleField, SelectField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_security.forms import RegisterForm

class SearchForm(FlaskForm):
    searchField = StringField()

class BookForm(FlaskForm):
    title = StringField(u'Title: ',validators=[DataRequired()])
    genre = StringField(u'Genre: ',validators=[DataRequired()])
    author = StringField(u'Author: ',validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField(u'Username: ',validators=[DataRequired()])
    password = PasswordField(u'Password: ',validators=[DataRequired()])

class RegisterUser(RegisterForm):
    first_name = StringField(u'First Name', validators=[DataRequired()])
    last_name = StringField(u'Last Name',validators=[DataRequired()])
    username = StringField(u'Username: ',validators=[DataRequired()])
    year = DateField(u'Year', validators=[DataRequired()])
    #genre_choices = [(g.genre) for g in Book.query.order_by('genre')]
    #author_choices = [(m.title) for m in Book.query.order_by('authors')]
    #genres = SelectMultipleField(u'Genres: ', coerce = int, choices = genre_choices)
    #authors = SelectMultipleField(u'Authors: ', coerce = int, choices  = author_choices)
