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
    return render_template('home.html')


@app.route('/vocab')
def vocab():
    return render_template('vocab.html', vocab=vocabulary)
