from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

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
                        
