"""
PackCheck - AI-Powered Food Label Verification System
Main application entry point
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import API blueprints
from api.scan import scan_bp
from api.nutrition import nutrition_bp
from api.verification import verification_bp
from api.personalization import personalization_bp
from api.community import community_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://localhost/packcheck')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(scan_bp, url_prefix='/api/scan')
    app.register_blueprint(nutrition_bp, url_prefix='/api/nutrition')
    app.register_blueprint(verification_bp, url_prefix='/api/verify')
    app.register_blueprint(personalization_bp, url_prefix='/api/personalize')
    app.register_blueprint(community_bp, url_prefix='/api/community')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'PackCheck API',
            'version': '1.0.0'
        })

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to PackCheck API',
            'endpoints': {
                'scan': '/api/scan',
                'nutrition': '/api/nutrition',
                'verification': '/api/verify',
                'personalization': '/api/personalize',
                'community': '/api/community'
            }
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'True') == 'True'
    )
