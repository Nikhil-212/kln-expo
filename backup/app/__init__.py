from flask import Flask
from flask_session import Session
import os

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev_key_12345'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.document import document_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(main_bp)

    return app

