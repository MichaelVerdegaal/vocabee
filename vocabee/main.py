import os

import werkzeug.exceptions
from flask import render_template

from vocabee import create_app

app = create_app()


@app.context_processor
def inject_env():
    return dict(GA_TRACKING_ID=os.getenv("GA_TRACKING_ID"))


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template("exceptions/400.html"), 400


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found_request(e):
    return render_template("exceptions/404.html"), 404


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_server_error_request(e):
    return render_template("exceptions/500.html"), 500
