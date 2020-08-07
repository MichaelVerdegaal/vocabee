import os

DEBUG = True  # Flask specific configs
TEMPLATE_DEBUG = False
CACHE_DEFAULT_TIMEOUT = 600
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('dbport')}/{os.getenv('database')}"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
