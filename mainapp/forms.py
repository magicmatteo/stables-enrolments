from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class EnrolmentForm(FlaskForm):
    studentfirstname = StringField('Student First Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    studentsurname = StringField('Student Surname', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    studentdob = DateField('Student Date of Birth (Format dd-mm-yyyy)', format='%d-%m-%Y')
    birth_cert = FileField('Upload birth certificate', validators=[FileAllowed(['jpg', 'pdf'])])

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    submit = SubmitField('Login')  

class RegisterForm(FlaskForm):
    code = StringField('Authorisation code', 
                                    validators=[DataRequired()])
    givenname = StringField('First Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                        validators=[DataRequired()])
    submit = SubmitField('Register')
                        
