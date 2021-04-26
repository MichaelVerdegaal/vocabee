from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from vocabee import cache

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@cache.cached(timeout=30)
def home():
    """
    Renders the home page
    :return: Webpage
    """
    try:
        return render_template("home/home.html")
    except TemplateNotFound:
        abort(404)


@home_bp.route('/about')
@cache.cached(timeout=30)
def about():
    """
    Renders the about page
    :return: Webpage
    """
    try:
        return render_template("home/about.html")
    except TemplateNotFound:
        abort(404)
