from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email

class newUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    file = FileField('Photo') #Make the file required