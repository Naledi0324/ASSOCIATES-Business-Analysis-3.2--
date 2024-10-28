#This file manages the main parts of the website, like the homepage and the user dashboard.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Medication, Reminder

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        # Medication form submission logic
        name = request.form.get('name')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not name or not dosage or not frequency or not start_date or not end_date:
            flash('All fields are required.', category='error')
        else:
            new_medication = Medication(name=name, dosage=dosage, frequency=frequency,
                                        start_date=start_date, end_date=end_date, user_id=current_user.id)
            db.session.add(new_medication)
            db.session.commit()
            flash('Medication added successfully!', category='success')
            
    adherence_data = {"adherence_times": [1, 2, 3, 4]}  # Example adherence data
    adherence_forecast = predict_medication_adherence(adherence_data)
    reminder_text = generate_reminder_text("MedicationName", "1 tablet", "8:00 AM")
    
    flash(f"Next dose reminder: {reminder_text}", "success")

    medications = Medication.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', medications=medications)

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/faq')
def faq():
    return render_template('faq.html')

@views.route('/privacy')
def privacy():
    return render_template('privacy.html')

@views.route('/terms')
def terms():
    return render_template('terms.html')
