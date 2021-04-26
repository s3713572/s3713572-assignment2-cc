from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from music.helpers.register_manager import is_email_exist


class LoginForm(FlaskForm):
    email = StringField('Email',
                              validators=[DataRequired(message=('Please enter your email'))])
    password = PasswordField('Password', validators=[DataRequired(message=('Please enter your password'))])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                              validators=[DataRequired(message=('Please enter your ID'))])
    user_name = StringField('Username',
                           validators=[DataRequired(message=('Please enter your username'))])

    password = PasswordField('Password', validators=[DataRequired(message=('Please enter your password'))])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message='Please confirm your password'), EqualTo('password')])

   
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if is_email_exist(email=email.data):
            raise ValidationError('That email is taken. Please choose a different one.')
