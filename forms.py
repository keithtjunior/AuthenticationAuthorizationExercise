from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DecimalField, BooleanField, TextAreaField, validators

class UserRegistrationForm(FlaskForm):
    """User registration WTForm data and validation"""
    username        = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    password        = PasswordField('Password', [validators.Length(min=8, max=256), validators.DataRequired()])
    email           = EmailField('Email', [validators.Length(min=5, max=50), validators.DataRequired()])
    first_name      = StringField('First Name', [validators.Length(min=1, max=30), validators.DataRequired()])
    last_name       = StringField('Last Name', [validators.Length(min=1, max=30), validators.DataRequired()])

class UserLoginForm(FlaskForm):
    """User login WTForm data and validation"""
    username        = StringField('Username', [validators.Length(min=1, max=20), validators.DataRequired()])
    password        = PasswordField('Password', [validators.Length(min=8, max=256), validators.DataRequired()])

class FeedbackCreateForm(FlaskForm):
    """Add feedback WTForm data and validation"""
    title    = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    content  = TextAreaField('Content', [validators.Length(min=1, max=280), validators.DataRequired()])

class FeedbackEditForm(FlaskForm):
    """Update feedback WTForm data and validation"""
    title    = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    content  = TextAreaField('Content', [validators.Length(min=1, max=280), validators.DataRequired()])
