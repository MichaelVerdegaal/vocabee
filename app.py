from flask import Flask, render_template
import file_util as fu

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/vocab')
def vocab():
    return render_template('vocab.html', vocab=fu.get_vocabulary())
