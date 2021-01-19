from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectMultipleField, SelectField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_security.forms import RegisterForm


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

class SearchBook(FlaskForm):
    book_search = StringField()

class BorrowForm(FlaskForm):
    book_borrow = SubmitField()

class ReturnForm(FlaskForm):
    book_return = SubmitField()

class changeUsernameForm(FlaskForm):
    change_username = SubmitField()
    new_username = StringField(u'New Username: ', validators = [DataRequired()])