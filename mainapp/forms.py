from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class EnrolmentForm(FlaskForm):
    child_given_names = StringField('Given Names', 
                                    validators=[DataRequired(), Length(min=2, max=40)])
    child_preferred_name = StringField('Preferred Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    child_family_name = StringField('Family Name', 
                                    validators=[DataRequired(), Length(min=1, max=20)])
    child_dob = DateField('Date of Birth (Format dd-mm-yyyy)', format='%d-%m-%Y')
    child_gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('not disclosed', 'Not Disclosed')],
                                    description='Childs gender')
    child_street = StringField('No. & Street', 
                                    validators=[DataRequired(), Length(max=60)])
    child_suburb = StringField('Suburb', 
                                    validators=[DataRequired(), Length(max=30)])
    child_state = StringField('State', 
                                    validators=[DataRequired(), Length(max=10)])
    child_postcode = StringField('Postcode', 
                                    validators=[DataRequired(), Length(min=4, max=4)])
    child_torres_strait = BooleanField('Torres Strait Islander')
    child_aboriginal = BooleanField('Aboriginal')


    
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
    given_name = StringField('First Name', 
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
                        
