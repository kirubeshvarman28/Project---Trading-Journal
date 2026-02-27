from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class AccountForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[Length(max=200)])
    balance = FloatField('Initial Balance', default=0.0)
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TradeForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()])
    entry_price = FloatField('Entry Price', validators=[DataRequired()])
    exit_price = FloatField('Exit Price', validators=[DataRequired()])
    lot_size = FloatField('Lot Size', validators=[DataRequired()])
    type = SelectField('Type', choices=[('Buy', 'Buy'), ('Sell', 'Sell')], validators=[DataRequired()])
    tag = StringField('Tag')
    notes = TextAreaField('Notes')
    screenshot = FileField('Screenshot')
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Log Trade')

class JournalForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    mood = StringField('Mood')
    mistakes = TextAreaField('Mistakes')
    lessons = TextAreaField('Lessons')
    notes = TextAreaField('Additional Notes')
    submit = SubmitField('Save Journal')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Note')

class PlaybookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rules = TextAreaField('Rules')
    risk_pct = FloatField('Risk %')
    screenshot = FileField('Typical Setup Screenshot')
    submit = SubmitField('Save Playbook')

class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link')
    category = StringField('Category')
    submit = SubmitField('Add Resource')
