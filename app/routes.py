from flask import (Blueprint, render_template,
                   flash, redirect, url_for, request)
from urllib.parse import urlsplit
from flask_login import (current_user, login_user,
                         logout_user, login_required)
import sqlalchemy as sa
from .models import db, User
from .forms import LoginForm, RegistrationForm, EditProfileForm
from datetime import datetime, timezone

# Define blueprint
routes_bp = Blueprint('routes', __name__)


# We define the routing here
# Index/landing page
@routes_bp.route('/')
@routes_bp.route('/index')
@login_required  # We require users to login before viewing this
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Diana'},
            'body': 'Que fuerte la película de Kimetsu no Yaiba'
        },
    ]

    return render_template('index.html', title='Home Page', posts=posts)


# Login page
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('routes.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# Logout page
@routes_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))


# Register form page
@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)


# User profile page
@routes_bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
            {'author': user, 'body': "Post prueba #1"},
            {'author': user, 'body': "Post prueba #2"}
    ]
    return render_template('user.html', user=user, posts=posts)


# Record time of last visit
@routes_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


# Profile editor page
@routes_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('routes.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
