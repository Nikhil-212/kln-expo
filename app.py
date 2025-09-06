
from flask import Flask, render_template, request, send_file, flash
from string import Template
import os
import spacy
from app.services.processor import LegalDocumentProcessor
import tempfile

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this in production
nlp = spacy.load('en_core_web_sm')
processor = LegalDocumentProcessor()

# Register blueprints
from app.routes import auth_bp, main_bp, document_bp
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(document_bp)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
