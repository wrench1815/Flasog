from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


def RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
