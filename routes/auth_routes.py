from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
from utils.email_service import send_welcome_email

auth_bp = Blueprint('auth', __name__)

from db import get_db

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    user_model = UserModel(db)
    if request.method == 'GET':
        return render_template('signup.html')
        
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    if not name or not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('auth.register'))

    result = user_model.create_user(name, email, phone, password)
    
    if result['success']:
        # Send welcome email asynchronously
        send_welcome_email(email, name, result['account_number'])
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(result['error'], 'error')
        return redirect(url_for('auth.register'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    db = get_db()
    user_model = UserModel(db)
    
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Email and password required.', 'error')
        return redirect(url_for('auth.login'))

    user = user_model.find_by_email(email)
    
    if user and user_model.verify_password(email, password):
        session['user_email'] = user['email']
        session['account_number'] = user['account_number']
        session['user_name'] = user['name']
        flash(f"Welcome back, {user['name']}!", 'success')
        return redirect(url_for('bank.dashboard'))
    else:
        flash('Invalid email or password.', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
