from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import LoginForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from .models import db, User

# Define blueprint
routes_bp = Blueprint('routes', __name__)


# We define the routing here
@routes_bp.route('/')
@routes_bp.route('/index')
def index():
    user = {'username': 'José'}
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
    return render_template('index.html', title='Home', user=user,
                           posts=posts)


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username is form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@routes_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
