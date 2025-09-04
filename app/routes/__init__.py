"""Routes package for the application."""
from flask import Blueprint

try:
    # Create blueprints
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    main_bp = Blueprint('main', __name__)

    # Import routes to register them with blueprints
    from . import auth_routes
    from . import main_routes

    # Import error handlers
    from . import errors
except Exception as e:
    print(f"Error in routes/__init__.py: {str(e)}")
    import traceback
    traceback.print_exc()
