"""
forms.py

We define how we handle forms for our Microblog
"""

from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
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
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sign In'))


# Registration form
class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
                         _l('Repeat Password'),
                         validators=[DataRequired(), 
                                     EqualTo('password')]
    )
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = db.session.scalar(
                sa.select(User).where(
                    User.username == username.data
                )
        )
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = db.session.scalar(
                sa.select(User).where(
                    User.email == email.data
                )
        )
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


# Profile edition form
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))


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
                raise ValidationError(_('Please use a different username.'))


# Empty form for following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))


# Blog submission form
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))


# Password reset request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


# Password reset form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'),
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
