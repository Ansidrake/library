from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
import os
from datetime import datetime, timedelta
from model import db,User,Book,Section,Feedback,BookAccess,BookRequest
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Optional
from app import app
from forms import RegistrationForm,LoginForm,BookForm,FeedbackForm,SectionForm

#from flask_charts import Chart, ChartData

def user_is_valid(username,password):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.password.data == password
    else:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if username and password are valid (You'll need to implement this logic)
        if form.username.data == 'librarian':
            return redirect(url_for('add_book'))
        elif user_is_valid(form.username.data, form.password.data):
            # Redirect to the user's profile page upon successful login
            return redirect(url_for('user_profile'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create a new user object with the form data
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)  # Assuming you have a method to hash the password
        db.session.add(new_user)
        db.session.commit()
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        form.confirm_password.data = ''   

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#librarian

@app.route('/book_details/<int:book_id>')
def book_details(book_id):
    # Retrieve the book details from the database
    book = Book.query.get(book_id)
    if book:
        return render_template('book_details.html', book=book)
    else:
        flash('Book not found.', 'danger')
        return redirect(url_for('librarian_books'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    #form.section_id.choices = [(section.id, section.name) for section in Section.query.all()]  # Populate section choices

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        content = form.content.data
        section_id = form.section_id.data
        price =  form.price.data
        
        new_book = Book(title=title, author=author, content=content, section_id=section_id, price=price)
        
        db.session.add(new_book)
        db.session.commit()

        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.section_id.data = ''
        form.price.data = ''
        flash('Book added successfully!', 'success')
        return redirect(url_for('librarian_books'))  # Assuming user_books is the route to display user's books
    return render_template('add_book.html', form=form)


@app.route('/librarian_books')
def librarian_books():
    # Retrieve all books from the database
    books = Book.query.all()
    return render_template('librarian_books.html', books=books)


@app.route('/book_requests')
def book_requests():
    # Retrieve all book requests from the database
    requests = BookRequest.query.all()
    return render_template('book_requests.html', requests=requests)

@app.route('/approve_request/<int:request_id>')
def approve_request(request_id):
    # Retrieve the book request from the database
    request = BookRequest.query.get(request_id)
    if request:
        # Add the requested book to the access database
        book_access = BookAccess(user_id=request.user_id, book_id=request.book_id)
        db.session.add(book_access)
        db.session.delete(request)  # Remove the request from the requests database
        db.session.commit()
        flash('Book request approved successfully.', 'success')
    else:
        flash('Book request not found.', 'danger')
    return redirect(url_for('book_requests'))

@app.route('/given_access')
def given_access():
    # Retrieve all books with access from the database
    books_with_access = BookAccess.query.all()
    # Create a list to store book details
    books = []
    # Iterate over books with access and fetch their details
    for access in books_with_access:
        book = Book.query.get(access.book_id)
        if book:
            books.append(book)
    return render_template('given_access.html', books=books)

@app.route('/revoke_access/<int:request_id>')
def revoke_access(request_id):
    # Retrieve the book access record from the database
    access = BookAccess.query.get(request_id)
    if access:
        db.session.delete(access)  # Remove the book access record
        db.session.commit()
        flash('Access revoked successfully.', 'success')
    else:
        flash('Book access record not found.', 'danger')
    return redirect(url_for('book_requests'))

@app.route('/sections')
def sections():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)

@app.route('/add_section', methods=['GET', 'POST'])
def add_section():
    form = SectionForm()
    if form.validate_on_submit():
        # Create a new section object with form data
        new_section = Section(
            name=form.name.data,
            description=form.description.data
        )
        # Add the new section to the database
        db.session.add(new_section)
        db.session.commit()
        flash('Section added successfully.', 'success')
        return redirect(url_for('sections'))  # Redirect to the next route after adding the section
    return render_template('add_section.html', form=form)

#@app.route('/statistics')
#def statistics():
#    total_books = Book.query.count()
#    total_sections = Section.query.count()
#
#    return render_template('statistics.html', total_books=total_books, total_sections=total_sections)



# user side



@app.route('/user_books/<int:user_id>')
def user_books(user_id):
    books = Book.query.all()
    return render_template('user_books.html', books=user_books, user_id = user_id)

@app.route('/search_user', methods=['POST'])
def search():
    search_query = request.form.get('search_query', '')
    # Query the database for books matching the search query
    books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    return render_template('search_results_user.html', books=books, search_query=search_query)

@app.route('/request_access/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def request_access(user_id,book_id):
    
    new_request = BookRequest(user_id= user_id,book_id=book_id)  # Assuming you are using Flask-Login for user authentication
    
    db.session.add(new_request)
    db.session.commit()
    flash('Access request sent successfully.', 'success')
    return redirect(url_for('user_books'))  # Redirect to the user's books page

@app.route('/user_books/<int:user_id>')
def accessed_books(user_id):
    # Query the book IDs associated with the user from the access database
    user_book_ids = db.session.query(BookAccess.book_id).filter_by(user_id=user_id).all()

    # Query the book details for the retrieved book IDs
    user_books = Book.query.filter(Book.id.in_(user_book_ids)).all()

    return render_template('access_books.html', books=user_books)

def remove_expired_access():
    # Calculate the date 7 days ago
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Query for books that were issued more than 7 days ago
    expired_access = BookAccess.query.filter(BookAccess.date_issued <= seven_days_ago).all()
    
    # Delete the expired access records
    for access in expired_access:
        db.session.delete(access)
    
    # Commit the changes to the database
    db.session.commit()


