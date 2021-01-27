import pymysql

import click
from flask import current_app, g
from flask.cli import with_appcontext
from main.config import db_info


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_info['host'],
            port=db_info['port'],
            user=db_info['user'],
            password=db_info['password'],
            db=db_info['database'],
            charset=db_info['charset'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )

    return g.db


def get_cursor():
    db = get_db()

    return db.cursor()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8mb4'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
