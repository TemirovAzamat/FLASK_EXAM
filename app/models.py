from flask_login import UserMixin

from . import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String)
    wage = db.Column(db.Integer, nullable=False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    position = db.relationship('Position', backref=db.backref('items', lazy='dynamic'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
