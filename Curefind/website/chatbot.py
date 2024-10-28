from flask import Blueprint, jsonify, request
from .nlp import analyze_user_input

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    user_text = request.json.get("message")
    response_text = analyze_user_input(user_text)
    return jsonify({"response": response_text})
