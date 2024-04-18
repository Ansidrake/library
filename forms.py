from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length,  EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    author = StringField('Author', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[InputRequired()])
    section_id = IntegerField('Section',validators=[InputRequired(), NumberRange(min=1)])  

class FeedbackForm(FlaskForm):
    comment = TextAreaField('Feedback', validators=[InputRequired()])

class SectionForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description')

