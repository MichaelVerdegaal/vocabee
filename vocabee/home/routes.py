import os
from pathlib import Path

import sass
from flask import Blueprint, render_template, abort, send_from_directory, request, Response
from jinja2 import TemplateNotFound

from vocabee.util.anki_util import create_deck_by_level
from vocabee.util.queries import get_vocab_by_level
from vocabee.util.vocabulary_util import process_vocabulary

home_bp = Blueprint('home',
                    __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/home')

sass.compile(dirname=('vocabee/home/static/sass', 'vocabee/home/static/css/'), output_style='compressed')


# Template routes
@home_bp.route('/')
def home():
    """
    Renders the home page
    :return: Webpage
    """
    try:
        return render_template("home.html")
    except TemplateNotFound:
        abort(404)


@home_bp.route('/vocab')
def vocab_index():
    """
    Renders the vocabulary level index page
    :return: Webpage
    """
    try:
        return render_template("vocab_index.html")
    except TemplateNotFound:
        abort(404)


@home_bp.route('/vocab/<int:vocab_level>')
def vocab(vocab_level):
    """
    Renders the vocabulary level datatables page
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: Webpage
    """
    if 0 < vocab_level < 6:
        try:
            return render_template("vocab.html", level=vocab_level)
        except TemplateNotFound:
            abort(404)
    else:
        try:
            return render_template("vocab_index.html")
        except TemplateNotFound:
            abort(404)


@home_bp.route('/deck')
def deck():
    """
    Renders the Anki deck page
    :return: Webpage
    """
    try:
        return render_template("deck.html")
    except TemplateNotFound:
        abort(404)


@home_bp.route('/about')
def about():
    """
    Renders the about page
    :return: Webpage
    """
    try:
        return render_template("about.html")
    except TemplateNotFound:
        abort(404)


# AJAX and download routes
@home_bp.route('/vocab/source/<int:vocab_level>')
def ajax_vocab(vocab_level):
    """
    AJAX endpoint to retrieve vocabulary
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: vocabulary in JSON
    """
    if 0 < vocab_level < 6:
        vocab = process_vocabulary(get_vocab_by_level(vocab_level))
        return vocab
    else:
        "Faulty vocabulary level"


@home_bp.route('/vocab/anki/<int:vocab_level>')
def get_anki_deck(vocab_level):
    """
    Creates download response for generated anki decks
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: downloaded file
    """
    vocab = get_vocab_by_level(vocab_level)
    project_root = Path(home_bp.root_path).parents[1]
    filename = f'vocabee{vocab_level}.apkg'

    path = os.path.join(project_root, filename)
    if not os.path.isfile(path):
        create_deck_by_level(vocab, vocab_level, filename)

    # Ref: https://stackoverflow.com/a/57998006/7174982
    with open(path, 'rb') as f:
        data = f.readlines()

    return Response(data, headers={
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': 'attachment; filename=%s;' % filename
    })


# Miscellaneous routes
@home_bp.route('/robots.txt')
@home_bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(home_bp.static_folder, request.path[1:])
