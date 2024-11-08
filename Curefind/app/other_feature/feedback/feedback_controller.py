# Logic for submitting and retrieving feedback
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Feedback, db
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET'])
@login_required
def get_feedbacks():
    """
    Get all feedbacks submitted by the current user.
    """
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).all()
    return jsonify([feedback.to_dict() for feedback in feedbacks]), 200

@feedback_bp.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    """
    Submit feedback from the user.
    """
    data = request.get_json()
    new_feedback = Feedback(
        user_id=current_user.id,
        content=data['content'],
        submitted_at=datetime.utcnow()
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify(new_feedback.to_dict()), 201

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['GET'])
@login_required
def get_feedback(feedback_id):
    """
    Get a specific feedback entry by ID.
    """
    feedback = Feedback.query.get_or_404(feedback_id)
    return jsonify(feedback.to_dict()), 200

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['DELETE'])
@login_required
def delete_feedback(feedback_id):
    """
    Delete an existing feedback entry.
    """
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback deleted successfully'}), 200

# Register the feedback blueprint in your main application
def register_feedback(app):
    app.register_blueprint(feedback_bp)
