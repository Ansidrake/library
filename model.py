from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app import app,db



class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=True)
    #books_accessed = db.relationship('BookAccess', backref='user', lazy=True)
    #def has_access_to_book(self, book_id):
    #    # Check if the user has access to the book based on the issue date
    #    book_access = BookAccess.query.filter_by(user_id=self.id, book_id=book_id).first()
    #    if book_access:
    #        return (datetime.utcnow() - book_access.issue_date) < timedelta(days=7)
    #    return False

class Book(db.Model):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    date_issued = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    feedback = db.relationship('Feedback', backref='book', lazy=True)
    requests = db.relationship('BookRequest', backref='book', lazy=True)

class Section(db.Model):
    __tablename__ = 'section'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    books = db.relationship('Book', backref='section', lazy=True)

    #section = db.relationship('Section', backref=db.backref('books', lazy=True))

class Feedback(db.Model):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class BookRequest(db.Model):
    __tablename__ = 'bookrequest'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)


class BookAccess(db.Model):
    __tablename__ = 'bookaccess'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def init_db():
    with app.app_context():
        db.create_all()
    


if __name__ == '__main__':
    init_db()
