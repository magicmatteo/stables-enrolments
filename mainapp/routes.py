from mainapp import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request
from mainapp.forms import EnrolmentForm, LoginForm, RegisterForm
from mainapp.models import User, Child
from mainapp.files import save_birth_cert, update_file_name
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import jsonify



@app.route('/')
def home():
    children = Child.query.filter_by(user_id=current_user.get_id())
    return render_template('home.html', children=children)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/enrol', methods=['GET', 'POST'])
@login_required
def enrol():
    form = EnrolmentForm()
    if form.validate_on_submit():
        child = Child(  given_names=form.child_given_names.data,
                        preferred_name=form.child_preferred_name.data,
                        family_name=form.child_family_name.data, 
                        dob=form.child_dob.data,
                        gender=form.child_gender.data,
                        street=form.child_street.data,
                        suburb=form.child_suburb.data,
                        state=form.child_state.data,
                        postcode=form.child_postcode.data,
                        torres_strait=form.child_torres_strait.data,
                        aboriginal=form.child_aboriginal.data,
                        birth_cert=form.birth_cert.data.filename,
                        user_id=current_user.get_id(),
                        date_created=datetime.now())
        
        ## Add child to get primary key to use in file name - then flush and re-add
        update_file_name(child, form.birth_cert.data)
        
        db.session.add(child)
        db.session.commit()
        
        flash('Successfully submitted', 'success')
        return redirect(url_for('home'))
    return render_template('enrol.html', title='Enrol', form=form)

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

@app.route('/api/v1/resources/children/all')
def api_child_all():
    children = {}
    c = Child.query.all()
    for x in c:
        children[x.id] = x.as_dict()
    return children