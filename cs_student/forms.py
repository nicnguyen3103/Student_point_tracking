from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddStudent(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    cohort = StringField('Cohort', validators=[DataRequired()])
    phone = StringField('Phone')
    email = StringField('Email')
    submit = SubmitField('Submit')