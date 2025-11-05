"""
Vercel serverless function entry point for PackCheck API
"""
import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from app import create_app

# Create the Flask app
app = create_app()

# Vercel serverless function handler
def handler(event, context):
    """Handler for Vercel serverless functions"""
    return app
