from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


def RegistrationForm(FlaskForm):
    userName = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    userEmail = StringField('Email', validators=[DataRequired(), Email()])
    userPassword = PasswordField('Password', validators=[DataRequired()])
    confirmUserPassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('userPassword')])
    submit = SubmitField('Sign Up')


def LoginForm(FlaskForm):
    userEmail = StringField('Email', validators=[DataRequired(), Email()])
    userPassword = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')
