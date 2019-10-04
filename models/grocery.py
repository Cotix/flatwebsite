from config import db, login_manager
import bcrypt


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    fetcher_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    text = db.Column(db.Text)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    fetched_date = db.Column(db.DateTime)

