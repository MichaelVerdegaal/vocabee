from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from vocabee import cache

vocabulary_bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')


@vocabulary_bp.route('/index')
@cache.cached(timeout=30)
def vocab_index():
    """
    Renders the vocabulary level index page
    :return: Webpage
    """
    try:
        return render_template("vocabulary/vocab_index.html")
    except TemplateNotFound:
        abort(404)


@vocabulary_bp.route('/browser/<int:vocab_level>')
@cache.cached(timeout=60)
def vocab_browser(vocab_level):
    """
    Renders the vocabulary level datatables page
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: Webpage
    """
    if 0 < vocab_level < 6:
        try:
            return render_template("vocabulary/browser.html", level=vocab_level)
        except TemplateNotFound:
            abort(404)
    else:
        try:
            return render_template("vocabulary/vocab_index.html")
        except TemplateNotFound:
            abort(404)


@vocabulary_bp.route('/deck')
@cache.cached(timeout=30)
def deck():
    """
    Renders the Anki deck page
    :return: Webpage
    """
    try:
        return render_template("vocabulary/deck.html")
    except TemplateNotFound:
        abort(404)