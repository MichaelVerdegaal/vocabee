from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from vocabee import cache

vocabulary_bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')


@vocabulary_bp.route('/index')
@cache.cached(timeout=30)
def vocabulary_index():
    """
    Renders the vocabulary level index page
    :return: Webpage
    """
    try:
        return render_template("vocabulary/vocabulary_index.html")
    except TemplateNotFound:
        abort(404)


@vocabulary_bp.route('/browser/<int:vocabulary_level>')
@cache.cached(timeout=60)
def vocabulary_browser(vocabulary_level):
    """
    Renders the vocabulary level datatables page
    :param vocabulary_level: Valid JLPT vocabulary level (1-5)
    :return: Webpage
    """
    if 0 < vocabulary_level < 6:
        try:
            return render_template("vocabulary/vocabulary_browser.html", level=vocabulary_level)
        except TemplateNotFound:
            abort(404)
    else:
        try:
            return render_template("vocabulary/vocabulary_index.html")
        except TemplateNotFound:
            abort(404)


@vocabulary_bp.route('/download')
@cache.cached(timeout=30)
def download_page():
    """
    Renders the download page
    :return: Webpage
    """
    try:
        return render_template("vocabulary/download_vocab.html")
    except TemplateNotFound:
        abort(404)


@vocabulary_bp.route('/searchresults')
@cache.cached(timeout=30)
def search_results():
    """
    Renders the search results page
    :return: Webpage
    """
    try:
        return render_template("vocabulary/search_results.html")
    except TemplateNotFound:
        abort(404)
