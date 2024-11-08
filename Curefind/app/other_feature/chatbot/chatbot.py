# Provides conversational support for health queries.
from flask import Flask, request, jsonify
import random
import spacy
from transformers import pipeline

app = Flask(__name__)

# Load SpaCy model for symptom detection
nlp = spacy.load("en_core_web_sm")

# Define intents and responses
intents = {
    "greeting": ["Hello! How can I assist you with your healthcare needs today?"],
    "appointment_schedule": ["I can help schedule an appointment. What date and time would you prefer?"],
    "appointment_cancel": ["To cancel an appointment, please provide your ticket number."],
    "doctor_inquiry": ["Which doctor would you like to see?"],
    "thank_you": ["You're welcome! Feel free to ask any other questions."],
    "symptom_inquiry": ["Please describe your symptoms to help me assist you further."],
    "prescription_refill": ["For a prescription refill, please provide the name of the medication."],
    "appointment_update": ["To update your appointment, provide your ticket number and the new details."],
    "location_inquiry": ["Can you specify the location you need?"],
    "operating_hours": ["We are open from 8 AM to 6 PM, Monday to Friday."],
    "emergency_contact": ["For emergencies, dial your local emergency services."],
    "default": ["I'm here to assist! Could you clarify your request?"]
}

# Initialize zero-shot classification model
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Classify user input into an intent
def classify_intent(message):
    labels = list(intents.keys())
    result = intent_classifier(message, labels)
    return result['labels'][0]

# Extract symptoms if user mentions any
def extract_symptoms(message):
    doc = nlp(message)
    symptoms = [token.text for token in doc if token.pos_ == 'NOUN']
    return symptoms

# Generate response based on intent
def respond_to_message(message):
    intent = classify_intent(message)
    response = random.choice(intents.get(intent, intents["default"]))
    
    # Add symptom detection if user is inquiring about symptoms
    if intent == "symptom_inquiry":
        symptoms = extract_symptoms(message)
        if symptoms:
            response += f" I noticed you mentioned: {', '.join(symptoms)}. I can assist you with finding a specialist for those symptoms."
    
    return response

# Define an API route for the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "I'm here to assist! Could you clarify your request?"})
    
    response = respond_to_message(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
