"""Authentication routes for the application."""
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_bp
from app.models import get_user, get_user_by_username, add_user
from app.models.history import add_user_history

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_username(username)
        if user and check_password_hash(user.get('password_hash', user.get('password', '')), password):
            # Store the actual user ID in session, not the username
            user_id = user.get('id')
            if user_id:
                session['user_id'] = user_id
                try:
                    add_user_history(user_id, 'login', 'User logged in')
                except Exception as e:
                    print(f"Failed to log user history: {e}")
                    # Continue with login even if history logging fails
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'success': True, 'redirect': url_for('main.index')}
            return redirect(url_for('main.index'))

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': False, 'error': 'Invalid username or password'}
        flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if get_user_by_username(username):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'success': False, 'error': 'Username already exists'}
            flash('Username already exists')
            return render_template('signup.html')

        user_data = add_user(username, generate_password_hash(password))
        if user_data:
            # user_data is a list of dicts, ensure correct access
            if isinstance(user_data, list) and len(user_data) > 0:
                try:
                    add_user_history(user_data[0]['id'], 'signup', 'User signed up')
                except Exception as e:
                    print(f"Failed to log user history: {e}")
                    # Continue with signup even if history logging fails
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'success': True, 'redirect': url_for('auth.login')}
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
