#Flask routes and API endpoints
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Reminder, Appointment, Feedback
from app.other_features.chatbot import respond_to_message
from app.ml_models import predict_health_data  # Placeholder for ML model function
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

# Home Route
@views.route('/')
def home():
    return render_template('home.html')


# Register Route
@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
            return redirect(url_for('views.register'))
        
        new_user = User(
            email=email,
            password=generate_password_hash(password, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account created!", category='success')
        return redirect(url_for('views.login'))
    
    return render_template('register.html')


# Login Route
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", category='success')
            return redirect(url_for('views.dashboard'))
        
        flash("Incorrect email or password.", category='error')
    
    return render_template('login.html')


# Dashboard Route
@views.route('/dashboard')
@login_required
def dashboard():
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'dashboard.html', 
        user=current_user, 
        reminders=reminders, 
        appointments=appointments
    )


# Logout Route
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category='info')
    return redirect(url_for('views.home'))


# Chatbot Endpoint
@views.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')
    chatbot_response = respond_to_message(user_message)
    return jsonify({'response': chatbot_response})


