from flask import render_template, flash, redirect, session, url_for, request, g, Blueprint
from flask_admin.contrib.sqla import ModelView
from models import User, Book
import flask_login
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from forms import RegisterUser, LoginForm, BookForm, SearchForm
from __init__ import db, app, login_manager, admin

main = Blueprint('main',__name__,
                    static_folder='static',
                    template_folder='templates')

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Book,db.session))

@main.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.dashboard"))
    return render_template("main.html", title = "Home") 

@main.route("/search", methods = ['GET','POST'])
def search_for_book():
    pass

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/registered', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'base.html',
        title='Dashboard | Personal Library',
        current_user=current_user
    )

@main_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("main.homepage"))

app.register_blueprint(main)
app.register_blueprint(main_bp)

#runs the app
if __name__ == "__main__":
    app.run(debug=True)