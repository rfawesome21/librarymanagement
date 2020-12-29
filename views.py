from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
from models import User
import flask_login
from flask_login import login_user, LoginManager, logout_user
from forms import RegisterUser, LoginForm, BookForm, UserForm
from __init__ import db,app


app.secret_key='12345'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route("/")
def homepage():
    return render_template("main.html", title = "Home")

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email = form.email.data).first()
        if existing_user is None:
            user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, user_name = form.username.data,
                year = form.year.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("homepage"))
        flash("A user already exists with that email address.")
    return render_template("registeruser.html", form = form, title = "Register")

@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(password = form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(url_for(next_page or 'homepage'))
        flash('Invalid username/password combination')
        return redirect(url_for("login"))
    return render_template("login.html",form = form, title = "Login") 

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

#runs the app
if __name__ == "__main__":
    app.run(debug=True)