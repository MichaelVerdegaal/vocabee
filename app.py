from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/<user>')
def hello_world(user=None):
    user = user or 'User'
    return render_template('index.html', user=user)