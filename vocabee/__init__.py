import os

from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

project_folder = os.path.expanduser('~/vocabee')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
    app.config.from_pyfile('config.py')
    db.init_app(app)
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)

    with app.app_context():
        from .home import home

        app.register_blueprint(home.home_bp)

        return app
