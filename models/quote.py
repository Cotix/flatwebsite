from config import db, login_manager
import bcrypt


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    text = db.Column(db.Text)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())



