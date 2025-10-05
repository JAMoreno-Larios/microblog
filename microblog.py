"""
A Microblog in Flask following Miguel Grinberg's tutorial.

Slightly modified by J. A. Moreno-Larios
2025
"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app
from app.models import db, User, Post, Message, Notification
from app.translate import translate

# Create Flask app instance
app = create_app()


# Define the shell context for interactive sessions
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post,
            'translate': translate, 'Message': Message,
            'Notification': Notification}
