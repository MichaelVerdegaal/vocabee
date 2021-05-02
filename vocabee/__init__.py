import os

import sass
from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery

project_folder = os.path.expanduser('~/vocabee')
load_dotenv(os.path.join(project_folder, '.env'))
# TODO make a constant for the static folder?

db = SQLAlchemy(query_class=CachingQuery)
cache = Cache(config={'CACHE_TYPE': 'simple'})
sass.compile(dirname=('vocabee/home/static/sass', 'vocabee/home/static/css/'), output_style='compressed')


def create_app():
    app = Flask(__name__, template_folder='home/templates/', static_folder='home/static/')
    cache.init_app(app)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from .home import models
        from .home.views import home, admin, miscellaneous
        from .home.views.vocabulary import vocabulary, vocabulary_ajax

        app.register_blueprint(home.home_bp)

        app.register_blueprint(vocabulary.vocabulary_bp)
        app.register_blueprint(vocabulary_ajax.vocabulary_ajax_bp)

        # app.register_blueprint(admin.admin_bp)

        app.register_blueprint(miscellaneous.miscellaneous_bp)

        return app
