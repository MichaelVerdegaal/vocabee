import os

import sass
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_minify import minify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery

from vocabee.config import PROJECT_FOLDER, APP_FOLDER, STATIC_FOLDER

load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))

db = SQLAlchemy(query_class=CachingQuery)
cache = Cache(config={'CACHE_TYPE': 'simple'})
sass.compile(dirname=(os.path.join(STATIC_FOLDER, 'sass'), os.path.join(STATIC_FOLDER, 'css')),
             output_style='compressed')


def create_app():
    app = Flask(__name__, template_folder='home/templates/', static_folder='home/static/')
    minify(app=app, html=True, js=True, cssless=False)
    cache.init_app(app)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from .home import models
        from .home.views import home, admin, miscellaneous
        from .home.views.vocabulary import vocabulary, vocabulary_ajax
        from .home.views.example import example_ajax

        app.register_blueprint(home.home_bp)

        app.register_blueprint(vocabulary.vocabulary_bp)
        app.register_blueprint(vocabulary_ajax.vocabulary_ajax_bp)
        app.register_blueprint(example_ajax.example_ajax_bp)

        app.register_blueprint(admin.admin_bp)

        app.register_blueprint(miscellaneous.miscellaneous_bp)

        return app
