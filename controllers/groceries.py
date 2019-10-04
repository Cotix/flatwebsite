import datetime

from flask import request, redirect, url_for
from flask_login import login_required, current_user

from config import app, db
from util import html
from models.grocery import Grocery


@app.route('/groceries', methods=['GET', 'POST'])
@login_required
def show_groceries():
    if request.method == 'POST':
        item_name = request.values.get('name')
        if item_name:
            db.session.add(Grocery(creator_id=current_user.id, text=item_name))
            db.session.commit()

    data = {
        'groceries': Grocery.query.filter(Grocery.fetched_date.is_(None)).all()
    }
    return html.ok('groceries', data)


@app.route('/groceries/<id>/delete', methods=['GET'])
@login_required
def delete_groceries(id):
    grocery = Grocery.query.get(id)
    if grocery:
        grocery.fetched_date = datetime.datetime.now()
        db.session.commit()
    return redirect(url_for('show_groceries'))
