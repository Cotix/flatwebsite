from flask_login import login_required

from config import *
from util import html


@app.route('/', methods=['GET'])
def index():
    return html.ok('index', {})


@app.route('/blog', methods=['GET'])
@login_required
def blog():
    return html.ok('blog', {})


@app.route('/quotes', methods=['GET'])
@login_required
def quotes():
    return html.ok('quotes', {})
