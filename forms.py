from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from dbmodels import User

class RegisterForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validate that the username is unique.
        """
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    """
    Form for file uploads.
    """
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Upload')

class EditAccessForm(FlaskForm):
    """
    Form for editing file access permissions.
    """
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField('Grant Access')
