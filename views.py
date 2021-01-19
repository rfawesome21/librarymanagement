from flask import render_template, flash, redirect, session, url_for, request, g, Blueprint, session
from flask_admin.contrib.sqla import ModelView
from models import User, Book
import flask_login
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from forms import RegisterUser, LoginForm, BookForm, SearchBook, BorrowForm, ReturnForm, changeUsernameForm
from __init__ import db, app, login_manager, admin
from datetime import datetime
from logging import FileHandler, WARNING
import logging

logging.basicConfig(filename='errorlog.txt',level = logging.DEBUG)


main = Blueprint('main',__name__,
                    static_folder='static',
                    template_folder='templates')

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Book,db.session))


#home page of the app
@main.route("/")
def homepage():
    form = SearchBook()
    book_of_the_day = Book.query.order_by(Book.userNumber.desc()).first()
    app.logger.info('Main Page')
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.dashboard"))
    return render_template("main.html", title = "Home", form = form, current_user = current_user, book_of_the_day = book_of_the_day) 


#shows search results of the books
@main.route("/results/<int:id>", methods = ['GET','POST'])
def search_results(id):
    form = SearchBook()
    form2 = BorrowForm()
    book = Book.query.get_or_404(id)
    title = book.name
    if form2.is_submitted():
        if not current_user.is_authenticated:
            flash("Please Login to borrow this book")
            app.logger.info('User Not Logged in!')   
            return render_template('search_results.html', form = form, book = book, form2 = form2, title = title, current_user = current_user)
        else:
            book.userNumber += 1
            book.date_borrowed = datetime.utcnow()
            book.user.append(current_user)
            app.logger.info('User logged in and borrowed a book')
            db.session.commit()
            return redirect(url_for('main_bp.returned'))
    return render_template('search_results.html', form = form, book = book, form2 = form2, title = title)


#shows the book you selected to borrow
@main.route("/search", methods = ['GET','POST'])
def search_for_book():
    form = SearchBook()
    if form.is_submitted():
        search = form.book_search.data
        flash(search)
        result = "%{}%".format(search)
        books = Book.query.filter(Book.name.like(result)).all()
        app.logger.info('Book Searched!')
        return render_template('results.html',books = books, form = form, current_user = current_user)
    return redirect(url_for('main.homepage'))

#shows all available books to borrow
@main.route("/viewbook")
def view_all_books():
    books = Book.query.all()
    form = SearchBook()
    return render_template('results.html', books = books, form = form, current_user = current_user)

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/registered', methods=['GET','POST'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    form = SearchBook()
    session['userID'] = current_user.id
    session['userName'] = current_user.username
    session['email'] = current_user.email
    book = Book.query.order_by(Book.id.desc()).limit(3)
    book_of_the_day = Book.query.order_by(Book.userNumber.desc()).first()
    if form.is_submitted():
        search = form.book_search.data
        flash(search)
        result = "%{}%".format(search)
        books = Book.query.filter(Book.name.like(result)).all()
        return render_template('results.html',books = books, form = form)
    return render_template(
        'loggedinuser.html',
        title='Dashboard | Personal Library',
        current_user=current_user,
        form = form,
        book = book,
        book_of_the_day = book_of_the_day
    )

@main_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    app.logger.info('Logged out')
    return redirect(url_for("main.homepage"))

#page to return books from
@main_bp.route('/return', methods = ['GET','POST'])
@login_required
def returned():
    form = SearchBook()
    form2 = ReturnForm()
    books = current_user.book
    return render_template(
        'return.html',
        title = 'Return a book',
        current_user = current_user,
        form = form,
        form2 = form2,
        books = books
    )

#return a book back to the library
@main_bp.route('/delete<int:id>',methods = ['POST','GET'])
@login_required
def delete(id):
    form2 = ReturnForm()
    if form2.is_submitted():
        flash(current_user.id)
        book = Book.query.get_or_404(id)
        user = User.query.filter_by(id=current_user.id).first()
        user.leave_book(book)
        db.session.commit()
        app.logger.info('Book Returned!')
        flash("Book returned successfully")
        return redirect(url_for('main_bp.returned'))
    return redirect(url_for("main_bp.returned"))
    
#session data
@main_bp.route('/get')
@login_required
def get_session():
    return str(session.get("email")) + str(session.get("userID")) + str(session.get("userName")) + str(session.get("books"))

#route to change your username
@main_bp.route('/user', methods = ['GET','POST'])
@login_required
def change_username():
    form = SearchBook()
    form2 = changeUsernameForm()
    if form2.is_submitted():
        current_user.username = form2.new_username.data
        db.session.commit()
        app.logger.info('Username Changed!')
        return redirect(url_for('main_bp.dashboard'))
    return render_template('change_username.html', form = form, form2 = form2)


app.register_blueprint(main)
app.register_blueprint(main_bp)


#runs the app
if __name__ == "__main__":
    app.run(debug=True)