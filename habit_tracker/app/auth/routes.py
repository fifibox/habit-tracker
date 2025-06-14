from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from habit_tracker.app import db, login_manager
from habit_tracker.app.models import User   # example model
from . import auth_bp
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        print("Form Data:", request.form)
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not username or not email or not password or not confirm_password:
            flash('All fields are required', 'signup')
            return redirect(url_for('auth.signup'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or not is_valid_email(email):
            flash('Invalid email address', 'signup')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash('Passwords do not match', 'signup')
            return redirect(url_for('auth.signup'))

        # Uniqueness checks
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'signup')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'signup')
            return redirect(url_for('auth.signup'))

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'signup')
            print(f"Error: {e}")
            return redirect(url_for('auth.signup'))
        login_user(user)
        flash('Signup successful! Welcome! You are signed in!', 'signup')
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        user_name = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=user_name).first()
        if not user:
            flash('User is not registered. Please sign up first.','auth_error')
            return redirect(url_for('main.home', show_login=True))

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'auth_success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password','auth_error')
            return redirect(url_for('main.home', show_login=True))
    return render_template('index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.','logout')
    return redirect(url_for('main.home'))
