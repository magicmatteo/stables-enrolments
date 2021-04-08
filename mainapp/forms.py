from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email

class EnrolmentForm(FlaskForm):
    child_given_names = StringField('Given Names', 
                                    validators=[DataRequired(), Length(min=2, max=40)])
    child_preferred_name = StringField('Preferred Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    child_family_name = StringField('Family Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    child_dob = DateField('Date of Birth (Format dd-mm-yyyy)', format='%d-%m-%Y')
    #child_gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('not disclosed', 'Not Disclosed')])
    child_street = StringField('No. & Street', 
                                    validators=[DataRequired(), Length(min=2, max=60)])

    
    birth_cert = FileField('Upload birth certificate', validators=[FileRequired(), FileAllowed(['jpg', 'pdf'])])

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
                        
