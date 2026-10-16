import sqlite3
import os
from flask import g, current_app
from config import Config

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE_PATH', Config.DATABASE_PATH)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app=None):
    """Initializes the database using schema.sql and seeds it if empty."""
    db_path = Config.DATABASE_PATH
    if app:
        db_path = app.config.get('DATABASE_PATH', Config.DATABASE_PATH)

    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    with open(schema_file, mode='r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()

    # Run seeder
    from seed_data import seed_all
    seed_all(conn)
    conn.close()

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)

    # Automatically initialize db if file doesn't exist
    db_path = app.config.get('DATABASE_PATH', Config.DATABASE_PATH)
    if db_path != ":memory:" and not os.path.exists(db_path):
        with app.app_context():
            init_db(app)
