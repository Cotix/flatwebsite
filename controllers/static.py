from config import *
from flask import send_from_directory


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
