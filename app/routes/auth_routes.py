"""Authentication routes for the application."""
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_bp
from ..models import users

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.get_user(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = username
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if users.get_user(username):
            flash('Username already exists')
            return render_template('signup.html')
        
        users.add_user(username, generate_password_hash(password))
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
