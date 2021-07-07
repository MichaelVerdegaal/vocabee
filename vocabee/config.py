import os

# Environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Project
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'vocabee')
STATIC_FOLDER = os.path.join(APP_FOLDER, 'home/static')

# Flask
DEBUG = False

# Caching
CACHE_DEFAULT_TIMEOUT = 60

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 180
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

# Flask-Security
SECRET_KEY = os.environ.get("SECRET_KEY")
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT" )
