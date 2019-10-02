from flask_login import login_user
from werkzeug.utils import redirect

from config import app, request, login_manager
from models.person import Person
from util import html


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return html.ok('login', {})

    name = request.values.get('username', '')
    password = request.values.get('password', '')

    user = Person.query.filter(Person.first_name == name).first()
    if user and user.check_password(password):
        login_user(user, remember=True)
        return redirect(request.values.get('next', '/'))

    return html.ok('login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
