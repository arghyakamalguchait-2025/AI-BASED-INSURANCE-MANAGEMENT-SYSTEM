import pytest

from app import create_app
from models import db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / 'test-insurance.db'
    test_app = create_app('default', {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{database_path.as_posix()}",
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret',
    })
    yield test_app
    with test_app.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
