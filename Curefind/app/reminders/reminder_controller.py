# Logic for setting and retrieving reminder
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Reminder, db
from datetime import datetime

reminder_bp = Blueprint('reminder', __name__)

@reminder_bp.route('/reminders', methods=['GET'])
@login_required
def get_reminders():
    """
    Get all reminders for the current user.
    """
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    return jsonify([reminder.to_dict() for reminder in reminders]), 200

@reminder_bp.route('/reminders', methods=['POST'])
@login_required
def create_reminder():
    """
    Create a new reminder.
    """
    data = request.get_json()
    
    new_reminder = Reminder(
        user_id=current_user.id,
        title=data['title'],
        description=data['description'],
        reminder_time=datetime.fromisoformat(data['reminder_time']),
        is_completed=False
    )
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify(new_reminder.to_dict()), 201

@reminder_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
@login_required
def update_reminder(reminder_id):
    """
    Update an existing reminder.
    """
    reminder = Reminder.query.get_or_404(reminder_id)
    
    if reminder.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    reminder.title = data['title']
    reminder.description = data['description']
    reminder.reminder_time = datetime.fromisoformat(data['reminder_time'])
    reminder.is_completed = data.get('is_completed', reminder.is_completed)
    
    db.session.commit()
    
    return jsonify(reminder.to_dict()), 200

@reminder_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
@login_required
def delete_reminder(reminder_id):
    """
    Delete a reminder.
    """
    reminder = Reminder.query.get_or_404(reminder_id)

    if reminder.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(reminder)
    db.session.commit()
    
    return jsonify({'message': 'Reminder deleted successfully'}), 200

# Register the reminder blueprint in your main application
def register_reminder(app):
    app.register_blueprint(reminder_bp)
