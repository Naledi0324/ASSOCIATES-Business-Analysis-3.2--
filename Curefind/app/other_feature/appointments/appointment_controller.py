# Logic for scheduling and retrieving appointments
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Appointment, db
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    """
    Get all appointments for the current user.
    """
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return jsonify([appointment.to_dict() for appointment in appointments]), 200

@appointments_bp.route('/appointments', methods=['POST'])
@login_required
def create_appointment():
    """
    Create a new appointment.
    """
    data = request.get_json()
    new_appointment = Appointment(
        user_id=current_user.id,
        title=data['title'],
        description=data['description'],
        appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S'),
        location=data['location']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@login_required
def get_appointment(appointment_id):
    """
    Get a specific appointment by ID.
    """
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(appointment.to_dict()), 200

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@login_required
def update_appointment(appointment_id):
    """
    Update an existing appointment.
    """
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    appointment.title = data.get('title', appointment.title)
    appointment.description = data.get('description', appointment.description)
    appointment.appointment_date = datetime.strptime(data.get('appointment_date', appointment.appointment_date.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
    appointment.location = data.get('location', appointment.location)

    db.session.commit()
    return jsonify(appointment.to_dict()), 200

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@login_required
def delete_appointment(appointment_id):
    """
    Delete an existing appointment.
    """
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'}), 200

# Register the appointments blueprint in your main application
def register_appointments(app):
    app.register_blueprint(appointments_bp)
