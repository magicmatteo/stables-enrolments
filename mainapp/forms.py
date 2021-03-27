from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class EnrolmentForm(FlaskForm):
    studentfirstname = StringField('Student First Name', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    studentsurname = StringField('Student Surname', 
                                    validators=[DataRequired(), Length(min=2, max=20)])
    studentdob = DateField('Student Date of Birth', format='%d-%m-%Y')
    submit = SubmitField('Submit')
                                    
