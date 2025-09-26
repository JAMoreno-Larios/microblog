from flask import Blueprint, render_template, flash, redirect, url_for
# from app import app
from .forms import LoginForm

# Define blueprint
routes_bp = Blueprint('routes', __name__)


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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
              form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
