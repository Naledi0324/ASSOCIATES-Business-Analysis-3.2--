# Logic for scheduling reminders
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import Reminder, db
from datetime import datetime
from flask import current_app

def send_reminder(reminder):
    """
    Function to send the reminder notification.
    This is a placeholder function. Replace with actual notification logic.
    """
    print(f"Reminder: {reminder.title}, Description: {reminder.description}")

def check_reminders():
    """
    Check for reminders that need to be sent.
    """
    with current_app.app_context():
        now = datetime.utcnow()
        reminders = Reminder.query.filter(Reminder.reminder_time <= now, Reminder.is_completed == False).all()
        
        for reminder in reminders:
            send_reminder(reminder)
            reminder.is_completed = True  # Mark as completed after sending
            db.session.commit()

def start_scheduler():
    """
    Start the background scheduler to check reminders.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_reminders, trigger="interval", minutes=1)  
    scheduler.start()
