import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
INSTANCE_DIR = PROJECT_ROOT / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = INSTANCE_DIR / 'insurance.db'

# Keep SQLite on the existing project database even if .env has a relative URI.
configured_database_url = os.getenv('DATABASE_URL', '')
database_uri = (
    configured_database_url
    if configured_database_url and not configured_database_url.startswith('sqlite:')
    else f"sqlite:///{DATABASE_PATH.as_posix()}"
)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_TIME_LIMIT = 3600


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
