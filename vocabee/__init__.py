import os

from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery

project_folder = os.path.expanduser('~/vocabee')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

db = SQLAlchemy(query_class=CachingQuery)
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
    cache.init_app(app)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from .home import routes, models

        db.create_all()
        db.session.commit()
        app.register_blueprint(routes.home_bp)

        return app
