from mainapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
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
