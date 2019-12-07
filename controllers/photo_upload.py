import os
from datetime import datetime

from flask import request, redirect, url_for
from flask_login import login_required, current_user
from wand.image import Image
from exif import Image as ExifImage
from config import app, db
from util import html, random
from models import Photo


def get_extension(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        return filename.rsplit('.', 1)[1].lower()


def categories():
    return [c[0] for c in db.session.query(Photo.category).distinct(Photo.category)]


def photo_upload_page(errors=[]):
    return html.ok('photos/photo_upload', {
        'categories': [c for c in categories()],
        'errors': errors
    })


def thumbnail(filename):
    with Image(filename=filename) as img:
        img.resize(400, int(img.height/img.width*400))
        img.crop(width=400, height=300, gravity='center')
        img.save(filename=filename+'.thumb.jpg')


@app.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def photo_upload():
    if request.method == 'GET':
        return photo_upload_page()

    category = request.values.get('category') or request.values.get('category_new')
    date = datetime.strptime(request.values.get('date'), '%Y-%m-%d')
    photos = request.files.getlist('photo')
    description = request.values.get('description')
    if not category or not date or not photos:
        errors = {'category': category, 'date': date, 'photo': photos}
        return photo_upload_page(errors=[k for k, v in errors.items() if not v])

    for photo in photos:
        try:
            exif = ExifImage(photo.stream)
            if exif.has_exif:
                date_str = exif.get('datetime_original') or exif.get('datetime')
                if date_str:
                    photo_date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                else:
                    photo_date = date
        except:
            photo_date = date

        photo.stream.seek(0)
        extension = get_extension(photo.filename)
        filename = f'{random.key(16)}.{extension}'
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        thumbnail(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(Photo(creator_id=current_user.id, category=category, description=description,
                             filename=filename, creation_date=photo_date))
        # Commit per photo in case upload fails halfway
        db.session.commit()

    return redirect(url_for('show_albums'))


@app.route('/photos', methods=['GET'])
@login_required
def show_albums():
    category_photo = {
        c: Photo.query.filter(Photo.category == c).first() for c in categories()
    }
    return html.ok('photos/show_photos', {
        'cards': [{'photo': p, 'text': c, 'href': f'/photos/album/{c}'} for c, p in category_photo.items()]
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
