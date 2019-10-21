from flask import request, redirect, url_for
from flask_login import login_required, current_user

from config import app, db
from util import html
from models.quote import Quote
from models.person import Person


@app.route('/quotes', methods=['GET', 'POST'])
@login_required
def show_quotes():
    if request.method == 'POST':
        text = request.values.get('text')
        author = request.values.get('author')
        if text and author:
            db.session.add(Quote(creator_id=current_user.id, text=text, author_id=int(author)))
            db.session.commit()
        return redirect(url_for('show_quotes'))

    page = int(request.values.get('page', 1))
    pagination = Quote.query.order_by(Quote.creation_date.desc()).paginate(page, per_page=25)
    data = {
        'quotes': pagination.items,
        'people': Person.query.all(),
        'pages': pagination,
    }
    return html.ok('quotes', data)
