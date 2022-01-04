from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASSWORD')}@{os.getenv('DBHOST')}:5432/{os.getenv('DBDATABASE')}"
app.config['SESSION_PROTECTION'] = 'strong' # for flask-login security 


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to view this page'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)
from mainapp.models import User, Child
db.create_all()
bcrypt = Bcrypt(app)



from mainapp import routes