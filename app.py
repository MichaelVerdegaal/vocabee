from flask import Flask, render_template
from flask_caching import Cache
from file_util import vocabulary

config = {
    "DEBUG": False,  # Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 600
}
app = Flask(__name__)
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
        return render_template("vocab.html", vocab=vocab)
    else:
        return render_template("vocab_index.html")
