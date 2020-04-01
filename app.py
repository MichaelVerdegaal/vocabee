from flask import Flask, render_template
from flask_caching import Cache
from file_util import vocabulary

config = {
    "DEBUG": False,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 600
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/vocab')
def vocab_index():
    return render_template("vocab_index.html")


@app.route('/vocab/<int:vocab_level>')
def vocab(vocab_level):
    if 0 < vocab_level < 6:
        vocab = vocabulary[vocab_level - 1]
        return render_template("vocab.html", vocab=vocab)
    else:
        return render_template("vocab_index.html")
