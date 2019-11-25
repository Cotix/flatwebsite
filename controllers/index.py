from flask_login import login_required
from flask import redirect

from config import *
from util import html


@app.route('/', methods=['GET'])
def index():
    return html.ok('index', {})


@app.route('/blog', methods=['GET'])
@login_required
def blog():
    return html.ok('blog', {})


@app.route('/eetlijst', methods=['GET'])
@login_required
def eetlijst():
    # Serving eetlijst in a iframe sounds like a good idea
    # But eetlijst is http only, which means we cant serve it on our https production version
    #return html.ok('eetlijst', {'eetlijst_url': app.config['EETLIJST_URL']})
    return redirect(app.config['EETLIJST_URL'])
