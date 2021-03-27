from mainapp import app
from flask import render_template, url_for, flash, redirect
from mainapp.forms import EnrolmentForm
from mainapp.models import User, Student

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/enrol', methods=['GET', 'POST'])
def enrol():
    form = EnrolmentForm()
    if form.validate_on_submit():
        flash('Successfully submitted', 'success')
        return redirect(url_for('home'))
    return render_template('enrol.html', title='Enrol', form=form)
