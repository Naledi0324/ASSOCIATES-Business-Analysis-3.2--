#Database models (SQLAlchemy)
from app import db
from datetime import datetime

class User(db.Model):
    """Model for users of the Curefind application."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    reminders = db.relationship('Reminder', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Reminder(db.Model):
    """Model for medication reminders."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    next_dose_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Reminder {self.medication_name} for User ID {self.user_id}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'appointment_date': self.appointment_date.isoformat(),
            'location': self.location
        }

class Feedback(db.Model):
    """Model for user feedback."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)

    def __repr__(self):
        return f'<Feedback from User ID {self.user_id} with Rating {self.rating}>'
