from config import db, login_manager
import bcrypt


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    _password = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

    def check_password(self, password):
        hash = self._password
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(user_id)
