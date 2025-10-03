"""
Flask Command-Line Interface custom commands
"""

from flask import Blueprint
import os
import click


# We use Blueprints to register commands
translate_bp = Blueprint('translate', __name__, cli_group='translate')
translate_bp.cli.short_help = "Translation and localization commands."
translate_bp.cli.help = "Translation and localization commands."


@translate_bp.cli.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate_bp.cli.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


@translate_bp.cli.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
