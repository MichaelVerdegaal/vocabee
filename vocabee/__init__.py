import os

import sass
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_minify import minify
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.models import fsqla_v2 as fsqla
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery

from vocabee.config import PROJECT_FOLDER, APP_FOLDER, STATIC_FOLDER

# Environment variables
load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))
# SQLAlchemy integration
db = SQLAlchemy(query_class=CachingQuery)
# Caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
# Compile SASS to CSS
sass.compile(dirname=(os.path.join(STATIC_FOLDER, 'sass'), os.path.join(STATIC_FOLDER, 'css')),
             output_style='compressed')
# Flask-Security setup
from .home.models import User, Role

fsqla.FsModels.set_db_info(db)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
    app = Flask(__name__, template_folder='home/templates/', static_folder='home/static/')
    minify(app=app, html=True, js=True, cssless=False)
    cache.init_app(app)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from .home import models
        from .home.views import home, admin
        from .home.views.vocabulary import vocabulary, vocabulary_ajax
        from .home.views.example import example_ajax
        from .home.views.user import user, user_ajax

        # Add url routes
        app.register_blueprint(home.home_bp)
        app.register_blueprint(vocabulary.vocabulary_bp)
        app.register_blueprint(user.user_bp)
        app.register_blueprint(admin.admin_bp)

        # Add AJAX routes
        app.register_blueprint(vocabulary_ajax.vocabulary_ajax_bp)
        app.register_blueprint(example_ajax.example_ajax_bp)
        app.register_blueprint(user_ajax.user_ajax_bp)

        # Flask-Security setup
        security = Security(app, user_datastore)

        return app
