from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '0f7b41806d2184aa62aaec6586dcfb7816e64a63755b57002230851e9db67275'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SESSION_PROTECTION'] = 'strong' # for flask-login security 
db = SQLAlchemy(app)
#from mainapp.models import User, Student
#db.create_all()
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to view this page'
login_manager.login_message_category = 'info'

from mainapp import routes