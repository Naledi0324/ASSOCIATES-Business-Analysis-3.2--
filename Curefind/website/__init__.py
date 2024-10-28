#This file puts the website together by loading settings and getting the database ready.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()  
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Ensure tables are created if they don't exist
    with app.app_context():
        db.create_all()

    # Import and register blueprints
    from .auth import auth
    from .views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app

# User loader for Flask-Login
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

