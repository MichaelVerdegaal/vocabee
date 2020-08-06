from flask import Blueprint, render_template

from vocabee.db_util import get_examples_by_id
from vocabee.file_util import get_vocabulary

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/')
def home():
    """
    Renders the home page
    :return: Webpage
    """
    return render_template("templates/home.html")


@home_bp.route('/vocab')
def vocab_index():
    """
    Renders the vocabulary level index page
    :return: Webpage
    """
    return render_template("vocab_index.html")


@home_bp.route('/vocab/<int:vocab_level>')
def vocab(vocab_level):
    """
    Renders the vocabulary level datatables page
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: Webpage
    """
    vocabulary = get_vocabulary()
    if 0 < vocab_level < 6:
        vocab = vocabulary[vocab_level - 1]
        return render_template("vocab.html", vocab=vocab, level=vocab_level)
    else:
        return render_template("vocab_index.html")


@home_bp.route('/vocab/example/<int:vocab_id>')
def vocab_get_examples(vocab_id):
    """
    AJAX endpoint to retrieve example sentences
    :param vocab_id: vocabulary entry id
    :return: examples in JSON
    """
    examples = get_examples_by_id(vocab_id)
    return examples
