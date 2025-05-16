from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class ShareHabitForm(FlaskForm):
    habit = SelectField('Choose a habit to share:', coerce=int, validators=[DataRequired()])
    recipient = StringField('Share with (username):', validators=[DataRequired()])
    submit = SubmitField('Share')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')