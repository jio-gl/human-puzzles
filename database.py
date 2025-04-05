import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def store_captcha(seed, expected_count):
    db = get_db()
    cursor = db.execute(
        'INSERT INTO captchas (seed, expected_count) VALUES (?, ?)',
        (seed, expected_count)
    )
    db.commit()
    return cursor.lastrowid

def store_response(captcha_id, user_count, ip_address):
    db = get_db()
    db.execute(
        'INSERT INTO responses (captcha_id, user_count, ip_address) VALUES (?, ?, ?)',
        (captcha_id, user_count, ip_address)
    )
    db.commit()

def get_captcha(captcha_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM captchas WHERE id = ?', (captcha_id,)
    ).fetchone()

def get_most_common_response(captcha_id):
    db = get_db()
    result = db.execute(
        '''
        SELECT user_count, COUNT(*) as count 
        FROM responses 
        WHERE captcha_id = ? 
        GROUP BY user_count 
        ORDER BY count DESC 
        LIMIT 1
        ''', 
        (captcha_id,)
    ).fetchone()
    
    if result is None:
        return None
    
    return result['user_count'] 