import mariadb
import json

import click
from flask import current_app, g

config = {
    'host': '10.10.1.25',
    'port': 3306,
    'user': 'root',
    'password': '3eaSss*7',
    'database': 'gehs_db'
}

def get_db():
    if 'db' not in g:
        g.db = mariadb.connect(
            # current_app.config['DATABASE'])
            **current_app.databaseConfig)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)