# Entry point to start the Flask application
from app import create_app, db
from app.models import User, Reminder, Appointment, Feedback  # Import models
from flask_migrate import Migrate
import sys
import os



app = create_app()

# Initialize the database and migration
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    """Create database tables before the first request."""
    db.create_all()

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/CorneresiaTherelious/Dropbox/PC/Desktop/Cureapp'))
if project_path not in sys.path:
    sys.path.append(project_path)

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
