import os
import tempfile
import pytest
from app import create_app
from config import Config
from db import init_db

@pytest.fixture
def app():
    # Create temporary database file for testing
    db_fd, db_path = tempfile.mkstemp()
    
    class TestAppConfig(Config):
        TESTING = True
        DATABASE_PATH = db_path
        SECRET_KEY = "test-secret-key"
        DEBUG = False

    app = create_app(TestAppConfig)

    with app.app_context():
        init_db(app)

    yield app

    os.close(db_fd)
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except PermissionError:
            pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_client(app):
    # Log in as demo pilgrim using a dedicated client
    c = app.test_client()
    c.post('/login', data={'login_id': 'pilgrim@yatra.in', 'password': 'pilgrim123'})
    return c

@pytest.fixture
def admin_client(app):
    # Log in as admin using a dedicated client
    c = app.test_client()
    c.post('/login', data={'login_id': 'admin@yatra.in', 'password': 'admin123'})
    return c
