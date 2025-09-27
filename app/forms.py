"""
forms.py

We define how we handle forms for our Microblog
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length
)
import sqlalchemy as sa
from .models import db, User


# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(
                sa.select(User).where(
                    User.username == username.data
                )
        )
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(
                sa.select(User).where(
                    User.email == email.data
                )
        )
        if user is not None:
            raise ValidationError('Please use a different email address.')


# Profile edition form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(
                sa.select(User).where(
                    User.username == username.data
                )
            )
        if user is not None:
            raise ValidationError('Please use a different username.')


# Empty form for following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
