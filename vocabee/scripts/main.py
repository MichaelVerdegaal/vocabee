import sass
from flask import Flask, render_template
from flask_caching import Cache

from vocabee.scripts.db_util import get_connection, get_cursor, get_examples_by_id
from vocabee.scripts.file_util import get_vocabulary

config = {
    "DEBUG": False,  # Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 600
}


def create_app():
    connection = get_connection()
    vocabulary = get_vocabulary(connection)

    sass.compile(dirname=('vocabee/static/sass', 'vocabee/static/css/'), output_style='compressed')
    app = Flask(__name__, template_folder='../templates/', static_folder='../static/')
    app.config.from_mapping(config)
    cache = Cache(app)

    @app.route('/')
    def home():
        """
        Renders the home page
        :return: Webpage
        """
        return render_template("home.html")

    @app.route('/vocab')
    def vocab_index():
        """
        Renders the vocabulary level index page
        :return: Webpage
        """
        return render_template("vocab_index.html")

    @app.route('/vocab/<int:vocab_level>')
    def vocab(vocab_level):
        """
        Renders the vocabulary level datatables page
        :param vocab_level: Valid JLPT vocabulary level (1-5)
        :return: Webpage
        """
        if 0 < vocab_level < 6:
            vocab = vocabulary[vocab_level - 1]
            return render_template("vocab.html", vocab=vocab, level=vocab_level)
        else:
            return render_template("vocab_index.html")

    @app.route('/vocab/example/<int:vocab_id>')
    def vocab_get_examples(vocab_id):
        """
        AJAX endpoint to retrieve example sentences
        :param vocab_id: vocabulary entry id
        :return: examples in JSON
        """
        cursor = get_cursor(connection)
        examples = get_examples_by_id(cursor, vocab_id)
        return examples

    return app
