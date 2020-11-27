import os

from dotenv import load_dotenv
from flask import Flask, _app_ctx_stack
from flask_caching import Cache
from sqlalchemy.orm import scoped_session

from .db_util import sessionLocal, engine

project_folder = os.path.expanduser('~/vocabee')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
    cache.init_app(app)

    with app.app_context():
        from .home import routes, models

        # Ref: https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
        app.session = scoped_session(sessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
        models.Base.metadata.create_all(bind=engine)
        models.Base.query = app.session.query_property()

        app.register_blueprint(routes.home_bp)

        return app
