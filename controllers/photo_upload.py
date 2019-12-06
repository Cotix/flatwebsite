import os
from datetime import datetime

from flask import request, redirect, url_for
from flask_login import login_required, current_user
from wand.image import Image

from config import app, db
from util import html, random
from models import Photo


def get_extension(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        return filename.rsplit('.', 1)[1].lower()


def categories():
    return [p for p in Photo.query.distinct(Photo.category).group_by(Photo.category)]


def photo_upload_page(errors=[]):
    return html.ok('photos/photo_upload', {
        'categories': [p.category for p in categories()],
        'errors': errors
    })


def thumbnail(filename):
    with Image(filename=filename) as img:
        img.resize(400, int(img.height/img.width*400))
        img.transform('400x300')
        img.save(filename=filename+'.thumb.jpg')


@app.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def photo_upload():
    if request.method == 'GET':
        return photo_upload_page()

    category = request.values.get('category') or request.values.get('category_new')
    date = datetime.strptime(request.values.get('date'), '%Y-%m-%d')
    photo = request.files.get('photo')
    description = request.values.get('description')
    extension = get_extension(photo.filename)
    if not category or not date or not photo or not extension:
        errors = {'category': category, 'date': date, 'photo': photo, 'extension': extension}
        return photo_upload_page(errors=[k for k, v in errors.items() if not v])
    filename = f'{random.key(16)}.{extension}'
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    thumbnail(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.session.add(Photo(creator_id=current_user.id, category=category, description=description,
                         filename=filename, creation_date=date))
    db.session.commit()

    return redirect(url_for('show_albums'))

@app.route('/photos', methods=['GET'])
@login_required
def show_albums():
    return html.ok('photos/show_photos', {
        'cards': [{'photo': p, 'text': p.category, 'href': f'/photos/album/{p.category}'} for p in categories()]
    })


@app.route('/photos/album/<album_id>', methods=['GET'])
@login_required
def show_album(album_id):
    return html.ok('photos/show_photos', {
        'cards': [{'photo': p, 'text': p.description, 'href': f'/photos/highres/{p.id}'}
                  for p in Photo.query.filter(Photo.category == album_id)]
    })


@app.route('/photos/highres/<photo_id>', methods=['GET'])
@login_required
def show_highres(photo_id):
    return html.ok('photos/show_highres', {
        'photo': Photo.query.get(int(photo_id))
    })
