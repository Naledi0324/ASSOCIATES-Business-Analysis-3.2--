 #Collects user inputs, validating and processing it for storage.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=200)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ReminderForm(FlaskForm):
    """Form for creating medication reminders."""
    medication_name = StringField('Medication Name', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = StringField('Frequency', validators=[DataRequired()])
    next_dose_time = DateTimeField('Next Dose Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Create Reminder')


class AppointmentForm(FlaskForm):
    """Form for creating appointments."""
    appointment_date = DateTimeField('Appointment Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    details = TextAreaField('Details')
    submit = SubmitField('Create Appointment')


class FeedbackForm(FlaskForm):
    """Form for submitting feedback."""
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')
