# This file handles user registration (sign-up), logging in, and logging out.
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Sign-up route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        # Input validation
        if len(username) < 2:
            flash('Username must be greater than 1 character.', category='Invalid')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='Invalid')
        elif password != repassword:
            flash('Passwords do not match.', category='Invalid')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='Invalid')
        else:
            user_exists = User.query.filter_by(username=username).first()

            if user_exists:
                flash('Username already exists.', category='Invalid')
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password)

                db.session.add(new_user)
                db.session.commit()

                flash('Account created successfully!', category='success')
                return redirect(url_for('views.dashboard'))

    return render_template('signup.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('views.dashboard'))

        flash('Invalid username or password.', category='Invalid')

    return render_template('login.html')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

