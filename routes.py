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
        return user.password == password
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
            user = User.query.filter_by(username=form.username.data).first()
            return redirect(url_for('owned_books',user_id = user.id))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = None
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username is already taken
        #existing_user = User.query.filter_by(username=form.username.data).first()
        #if existing_user:
        #    flash('Username is already taken. Please choose a different one.', 'error')
        #    return redirect(url_for('register'))

        # Create a new user object with the form data
        new_user = User(username=form.username.data,password = form.password.data,role = 'User')
        db.session.add(new_user)
        db.session.commit()
        form.username.data = ''
        form.password.data = ''
        form.confirm_password.data = ''   

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#librarian

@app.route('/book_details/<int:book_id>')
def book_details(book_id):
    # Retrieve the book details from the database
    book = Book.query.get_or_404(book_id)
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
        
        
        new_book = Book(title=title, author=author, content=content, section_id=section_id)
        
        db.session.add(new_book)
        db.session.commit()

        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.section_id.data = ''
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('librarian_books'))  # Assuming owned_books is the route to display user's books
    return render_template('add_book.html', form=form)


@app.route('/librarian_books')
def librarian_books():
    books = Book.query.all()
    return render_template('librarian_books.html', books=books)
    #except:
    #    flash('No Books are available!')
    #    return redirect(url_for('add_book'))


@app.route('/book_requests')
def book_requests():
    
    try:
        requests = BookRequest.query.all()
        return render_template('book_requests.html', requests=requests)
    except:
        flash('No Boooks are requested!!')
        return redirect(url_for(librarian_books))

#@app.route('/approve_request/<int:request_id>')
#def approve_request(request_id):
#    # Retrieve the book request from the database
#    request = BookRequest.query.get_or_404(request_id)
#    
#    if request is not None:
#    # Your existing logic here
#
#        # Check if the book is already approved
#        existing_access = BookAccess.query.filter_by(user_id=request.user_id, book_id=request.book_id).first()
#        if existing_access:
#            flash('Book request already approved.', 'warning')
#            db.session.delete(request)  # Remove the request from the requests database
#            db.session.commit()
#        else:
#            # Add the requested book to the access database
#            user_id=request.user_id
#            book_id=request.book_id
#            book_access = BookAccess(user_id=user_id, book_id=book_id)
#            db.session.add(book_access)
#            db.session.delete(request)  # Remove the request from the requests database
#            db.session.commit()
#            flash('Book request approved successfully.', 'success')
#    else:
#        flash('Book request not found.', 'danger')
#    return redirect(url_for('book_requests'))
@app.route('/approve_request/<int:request_id>')
def approve_request(request_id):
    request = BookRequest.query.get_or_404(request_id)

    if request is not None:
        existing_access = BookAccess.query.filter_by(user_id=request.user_id, book_id=request.book_id).first()
        if existing_access:
            flash('Book request already approved.', 'warning')
            db.session.delete(request)
            db.session.commit()
        else:
            try:
                user_id = request.user_id
                book_id = request.book_id
                book_title = Book.query.get(book_id).title
                print(f"User ID: {user_id}, Book ID: {book_id}")  # Debug message
                book_access = BookAccess(user_id=user_id, book_id=book_id)
                db.session.add(book_access)
                db.session.delete(request)
                db.session.commit()
                flash(f'Book request for "{book_title}" approved successfully.', 'success')
                
                # Debugging: Check if the access record is added to the database
                access_record = BookAccess.query.filter_by(user_id=user_id, book_id=book_id).first()
                if access_record:
                    print("Access record added successfully:", access_record)
                else:
                    print("Access record not found in the database.")
            except Exception as e:
                flash('An error occurred while processing the request. Please try again later.', 'danger')
                print(f'Error: {e}')
    else:
        flash('Book request not found.', 'danger')
    return redirect(url_for('book_requests'))



@app.route('/book_access')
def book_access():
    #try:
    access = BookAccess.query.all()
    return render_template('book_access.html', access = access)
    #except:
    #    flash('No Boooks are given!!')
    #    return redirect(url_for('librarian_books'))


@app.route('/revoke_access/<int:access_id>')
def revoke_access(access_id):
    # Retrieve the book access record from the database
    access = BookAccess.query.get_or_404(access_id)
    if access:
        db.session.delete(access)  # Remove the book access record
        db.session.commit()
        flash('Access revoked successfully.', 'success')
    else:
        flash('Book access record not found.', 'danger')
    return redirect(url_for('book_access'))

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



@app.route('/all_books/<int:user_id>')
def all_books(user_id):
    books = Book.query.all()
    user = User.query.filter_by(id = user_id ).first()
    return render_template('all_books.html', books=books, user_id = user.id,user=user)

@app.route('/search_user', methods=['POST'])
def search():
    search_query = request.form.get_or_404('search_query', '')
    # Query the database for books matching the search query
    books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    return render_template('search_results_user.html', books=books, search_query=search_query)

@app.route('/request_access/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def request_access(user_id, book_id):
    # Check if the book has already been requested by the user
    existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id).first()

    if existing_request:
        flash('Access request for this book has already been sent.', 'error')
    else:
        new_request = BookRequest(user_id=user_id, book_id=book_id)
        db.session.add(new_request)
        db.session.commit()
        flash('Access request sent successfully.', 'success')

    return redirect(url_for('user_sections', user_id=user_id)) # Redirect to the user's books page

@app.route('/owned_books/<int:user_id>')
def owned_books(user_id):
    # Query the book accesses associated with the user from the database
    access = BookAccess.query.filter_by(user_id=user_id).all()
    
    user = User.query.filter_by(id=user_id).first()
    
    return render_template('owned_books.html', access=access, user=user)


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

@app.route('/user_sections/<int:user_id>')
def user_sections(user_id):
    sections = Section.query.all()
    user = User.query.filter_by(id = user_id).first()
    return render_template('user_sections.html', sections=sections, user = user,user_id = user.id)

@app.route('/user_profile.<int:user_id>')
def user_profile(user_id):
    user = User.query.filter_by(id = user_id ).first()
    return redirect(url_for('owned_books',user = user,user_id = user.id))

@app.route('/')
def index():
    return redirect(url_for('login'))

#@app.route('/all_books/<int:user_id>')
#def all_books(user_id):
#    books = Book.query.all()
#    return render_template('all_books.html', books=books,user_id = user_id)
#    #except: