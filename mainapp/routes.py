from mainapp import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from mainapp.forms import EnrolmentForm, LoginForm, RegisterForm
from mainapp.models import User, Child
from mainapp.files import update_file_name
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from mainapp.config import config
import psycopg2


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
                        birth_cert=form.birth_cert.data,
                        user_id=current_user.get_id(),
                        date_created=datetime.now())
        
        ## Add child to get primary key to use in file name - then flush and re-add
        if form.birth_cert.data:
            update_file_name(child, form.birth_cert.data)
        else:
            child.birth_cert = None
        
        db.session.add(child)
        db.session.commit()
        
        flash('Successfully submitted', 'success')
        return redirect(url_for('home'))
    return render_template('enrol.html', title='Enrol', form=form)

@app.route('/sql', methods=['GET', 'POST'])
@login_required
def sql():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute('SELECT * FROM child')

        # display the PostgreSQL database server version
        children = cur.fetchall()
        columns = cur.description
        colnames = [col[0] for col in columns]
        print(colnames)

        children_list = []
            
        for child in children:
            n = {}
            for x, y in zip(child, colnames):
                n[y] = x
            children_list.append(n)

        cur.close()
        
        return render_template('sql.html', title='SQL - No ORM', db_version=children_list)

       
	# close the communication with the PostgreSQL
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

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

@app.route('/api/v1/resources/children/add', methods=['POST'])
def api_add_child():
    if not request.json:
        abort(400)
    
    # if not current_user.is_authenticated:
    #     return ('Not logged in', 401)

    child = Child(  preferred_name = request.json['preferred_name'],
                    given_names = request.json['given_names'],
                    family_name = request.json['family_name'],
                    dob = datetime.strptime(request.json['dob'], '%d-%m-%Y').date(),
                    gender = request.json['gender'],
                    street = request.json['street'],
                    suburb = request.json['suburb'],
                    state = request.json['state'],
                    postcode = request.json['postcode'],
                    torres_strait = request.json['torres_strait'],
                    aboriginal = request.json['aboriginal'],
                    birth_cert = None,
                    date_created = datetime.now(),
                    user_id = request.json['user_id']
                    )
    parent = User.query.get(child.user_id)
    db.session.add(child)
    db.session.commit()
    return jsonify({'Name': child.given_names + ' ' + child.family_name,
                    'Time Created': child.date_created,
                    'Parent': parent.email }), 201

@app.route('/api/v1/resources/children/delete/<int:id>', methods=['POST'])
def api_delete_child(id):
    c = Child.query.get(id)
    if c:
        try:
            db.session.delete(c)
            db.session.commit()
            flash("User deleted successfully", 'info')
            # children = Child.query.filter_by(user_id=current_user.get_id())
            # return (render_template('home.html', children=children), 201)
            return redirect(url_for('home'))
        except:
            flash('Error - please contact administrator', 'danger')
            return redirect(url_for('home'))
    
    flash('Resource not found - please contact administrator', 'danger')
    return redirect(url_for('home'))

@app.route('/api/v1/resources/children/details/<int:id>', methods=['GET'])
def api_details_child(id):
    c = Child.query.get(id)
    if c:
        return (c.as_dict(), 200)
    return ('Error 404 - Resource not found in the database', 404)