from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
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
