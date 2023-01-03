from mainapp import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request
from mainapp.forms import LoginForm, RegisterForm
from mainapp.models import User
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import requests
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session

CLIENT_ID = r'xxx'
CLIENT_SECRET = r'xxx'
TOKEN_URL = r'https://bitbucket.org/site/oauth2/access_token'
token = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/scripts')
def scripts():
    global token
    client = BackendApplicationClient(client_id=CLIENT_ID)
    session = OAuth2Session(client=client)
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    if 'access_token' not in token:
        print('token not present - fetching...')
        token = session.fetch_token(token_url=TOKEN_URL, auth=auth)
    i = 0
    while i <= 3:
        try:
            if session.access_token == None:
                print(f'session has no token - setting global token..')
                session.token = token
            commit_id = get_commit_id('master', session)
            print(f'Commit ID: {commit_id}')
            files = get_bitbucket_files(commit_id, session)
            print(f'{files}')
            break
        except TokenExpiredError as e:
            token = session.refresh_token(TOKEN_URL)
            i += 1
    
    session.close()
    return render_template('scripts.html', title='Scripts')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful.', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.code.data == 'code':
            if form.password.data == form.confirm_password.data:
                user_exist = User.query.filter_by(email=form.email.data).first()
                if not user_exist:
                    hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    user = User(firstname=form.given_name.data, 
                                surname=form.surname.data, 
                                email=form.email.data, password=hashed_pw,
                                date_created=datetime.now())
                    db.session.add(user)
                    db.session.commit()
                    flash('Successfully registered - please login.', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('User already exists.', 'danger')
                    return redirect(url_for('register'))
            else:
                form.confirm_password.errors.append('Passwords do not match')
                form.password.errors.append('Passwords do not match')
        else:
            flash('Invalid authorisation code!', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    user = User.query.get(current_user.get_id())
    return render_template('account.html', title='Account', user=user)

def get_commit_id(branch_name :str, oauth_session :OAuth2Session):
    url = f'https://api.bitbucket.org/2.0/repositories/magicmatteo/query-able-scripts/refs/branches/{branch_name}'
    r = oauth_session.get(url)
    return r.json()['target']['hash'][0:7]

def get_bitbucket_files(commit_id :str, oauth_session :OAuth2Session):
    ''' Returns a list of SQL scripts in the repo that are approved for running.'''

    url = f'https://api.bitbucket.org/2.0/repositories/magicmatteo/query-able-scripts/src/{commit_id}/sql/'
    r = oauth_session.get(url)
    json = r.json()
    files = []
    for i in json['values']:
        files.append(i['path'])
    return files