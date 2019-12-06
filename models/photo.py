from config import db, login_manager
import bcrypt


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    creator = db.relationship('Person', foreign_keys=[creator_id])

    category = db.Column(db.Text)
    description = db.Column(db.Text)
    filename = db.Column(db.Text, unique=True)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

