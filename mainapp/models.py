from mainapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    children = db.relationship('Student', backref='parent', lazy=True)

    def __repr__(self):
        return f"User({self.email})"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    givenname = db.Column(db.String(20), nullable=False)
    givenname2 = db.Column(db.String(30), nullable=True)
    surname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Student({self.givenname} {self.surname})"