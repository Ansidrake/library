from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Optional


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
    section_id = IntegerField('Section',validators=[InputRequired(), NumberRange(min=1)])  # Assuming you have a list of sections to select from
    

class FeedbackForm(FlaskForm):
    comment = TextAreaField('Feedback', validators=[InputRequired()])

class SectionForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description')

