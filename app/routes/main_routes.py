"""Main application routes."""
from flask import render_template, session
from . import main_bp
from ..models import users

@main_bp.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = users.get_user(session['user_id'])
    return render_template('index.html', user=user)
