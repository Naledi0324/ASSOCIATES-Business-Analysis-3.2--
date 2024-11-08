#initialize the flask app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from app.reminders.reminder_controller import register_reminder
from app.other_features.feedback.feedback_controller import register_feedback
from app.other_features.chatbot import register_chatbot
from app.reminders.reminder_scheduler import start_scheduler

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    register_reminder(app)
    register_feedback(app)
    register_chatbot(app)

    # Start the reminder scheduler
    start_scheduler()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app
