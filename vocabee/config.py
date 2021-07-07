import os

# Project
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'vocabee')
STATIC_FOLDER = os.path.join(APP_FOLDER, 'home/static')

# Flask
DEBUG = False

# Caching
CACHE_DEFAULT_TIMEOUT = 60

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 180
SQLALCHEMY_POOL_SIZE = 20
