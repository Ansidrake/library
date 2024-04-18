from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
import os
from datetime import datetime, timedelta
from model import db,User,Book,Section,Feedback,BookAccess,BookRequest
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Optional
from app import app
from forms import RegistrationForm,LoginForm,BookForm,FeedbackForm,SectionForm




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

        if form.username.data == 'librarian':
            return redirect(url_for('add_book'))
        elif user_is_valid(form.username.data, form.password.data):

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

        new_user = User(username=form.username.data,password = form.password.data,role = 'User')
        db.session.add(new_user)
        db.session.commit()
        form.username.data = ''
        form.password.data = ''
        form.confirm_password.data = ''   

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/book_details/<int:book_id>')
def book_details(book_id):

    book = Book.query.get_or_404(book_id)
    if book:
        return render_template('book_details.html', book=book)
    else:
        flash('Book not found.', 'danger')
        return redirect(url_for('librarian_books'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

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
        return redirect(url_for('librarian_books'))  
    return render_template('add_book.html', form=form)


@app.route('/librarian_books')
def librarian_books():
    books = Book.query.all()
    return render_template('librarian_books.html', books=books)
    


@app.route('/book_requests')
def book_requests():
    try:
        requests = BookRequest.query.all()
        return render_template('book_requests.html', requests=requests)
    except:
        flash('No Boooks are requested!!')
        return redirect(url_for(librarian_books))

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
               
                book_access = BookAccess(user_id=user_id, book_id=book_id)
                db.session.add(book_access)
                db.session.delete(request)
                db.session.commit()
                flash(f'Book request for "{book_title}" approved successfully.', 'success')
                
                access_record = BookAccess.query.filter_by(user_id=user_id, book_id=book_id).first()
                
            except Exception as e:
                flash('An error occurred while processing the request. Please try again later.', 'danger')

    else:
        flash('Book request not found.', 'danger')
    return redirect(url_for('book_requests'))



@app.route('/book_access')
def book_access():
    access = BookAccess.query.all()
    return render_template('book_access.html', access = access)
    

@app.route('/revoke_access/<int:access_id>')
def revoke_access(access_id):
    access = BookAccess.query.get_or_404(access_id)
    if access:
        db.session.delete(access)
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
        new_section = Section(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_section)
        db.session.commit()
        flash('Section added successfully.', 'success')
        return redirect(url_for('sections')) 
    return render_template('add_section.html', form=form)

@app.route('/all_books/<int:user_id>')
def all_books(user_id):
    books = Book.query.all()
    user = User.query.filter_by(id = user_id ).first()
    return render_template('all_books.html', books=books, user_id = user.id,user=user)

@app.route('/search_user', methods=['POST'])
def search():
    search_query = request.form.get_or_404('search_query', '')
    books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    return render_template('search_results_user.html', books=books, search_query=search_query)

@app.route('/request_access/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def request_access(user_id, book_id):
    existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id).first()

    if existing_request:
        flash('Access request for this book has already been sent.', 'error')
    else:
        new_request = BookRequest(user_id=user_id, book_id=book_id)
        db.session.add(new_request)
        db.session.commit()
        flash('Access request sent successfully.', 'success')

    return redirect(url_for('user_sections', user_id=user_id)) 

@app.route('/owned_books/<int:user_id>')
def owned_books(user_id):
    access = BookAccess.query.filter_by(user_id=user_id).all()
    
    user = User.query.filter_by(id=user_id).first()
    
    return render_template('owned_books.html', access=access, user=user)


def remove_expired_access():
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    expired_access = BookAccess.query.filter(BookAccess.date_issued <= seven_days_ago).all()
    for access in expired_access:
        db.session.delete(access)
    
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
