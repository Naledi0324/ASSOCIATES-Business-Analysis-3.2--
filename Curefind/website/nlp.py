import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
text_generator = pipeline("text-generation", model="gpt-2")

def generate_reminder_text(medication_name, dosage, time):
    reminder_text = f"Remember to take {dosage} of {medication_name} at {time}."
    return text_generator(reminder_text, max_length=30)[0]['generated_text']

def analyze_user_input(user_text):
    doc = nlp(user_text)
    if "reminder" in user_text:
        return "Would you like me to set a reminder for your medication?"
    # More intent checks can be added here
    return "How can I assist you with your medication?"
