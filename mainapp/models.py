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
    children = db.relationship('Child', backref='parent', lazy=True)
    

    def __repr__(self):
        return f"User({self.email})"

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preferred_name = db.Column(db.String(20), nullable=False)
    given_names = db.Column(db.String(40), nullable=False)
    family_name = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(15), nullable=False)

    # Child Address
    street = db.Column(db.String(60), nullable=False)
    suburb = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    postcode = db.Column(db.String(4), nullable=False)

    torres_strait = db.Column(db.Boolean, nullable=False)
    aboriginal = db.Column(db.Boolean, nullable=False)

    # File uploads
    birth_cert = db.Column(db.String(60), nullable=False)
    
    # Metadata
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"Child({self.givenname} {self.surname})"