import os

import sass
from dotenv import load_dotenv
from flask import Flask, render_template_string
from flask_caching import Cache
from flask_minify import minify
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v2 as fsqla
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery

from vocabee.config import PROJECT_FOLDER, APP_FOLDER, STATIC_FOLDER

# Environment variables
load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))
# SQLAlchemy integration
db = SQLAlchemy(query_class=CachingQuery)
# Flask-Security setup
fsqla.FsModels.set_db_info(db)
# Caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
# Compile SASS to CSS
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
        from .home.views import home, admin
        from .home.views.vocabulary import vocabulary, vocabulary_ajax
        from .home.views.example import example_ajax

        app.register_blueprint(home.home_bp)
        app.register_blueprint(vocabulary.vocabulary_bp)
        app.register_blueprint(vocabulary_ajax.vocabulary_ajax_bp)
        app.register_blueprint(example_ajax.example_ajax_bp)
        # app.register_blueprint(admin.admin_bp)

        # Flask-Security setup
        user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
        security = Security(app, user_datastore)

        @app.before_first_request
        def create_user():
            db.create_all()
            if not user_datastore.find_user(email="test@me.com"):
                user_datastore.create_user(email="test@me.com", password=hash_password("password"))
            db.session.commit()

        # Views
        @app.route("/hi")
        @auth_required()
        def home():
            return render_template_string("Hello {{ current_user.email }}")

        return app
