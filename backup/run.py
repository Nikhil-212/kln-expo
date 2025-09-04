#!/usr/bin/env python3
"""
Legal Document Generator - Startup Script
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def install_spacy_model():
    """Install spaCy English model"""
    print("🔤 Installing spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install spaCy model")
        return False

def run_application():
    """Run the Flask application"""
    print("🚀 Starting Legal Document Generator...")
    print("📍 Application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("📄 Legal Document Generator")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Install spaCy model
    if not install_spacy_model():
        sys.exit(1)
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main() 