from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from config import config
from models import db
from routes.auth import auth_bp
from routes.products import products_bp
from routes.reviews import reviews_bp
from routes.salts import salts_bp
from routes.config import config_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])
    
    # Enable request logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:3001', 'http://127.0.0.1:3001'])
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is required'}), 401
    
    # Basic home route
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to Medingen Backend API',
            'status': 'running',
            'endpoints': {
                'login': '/api/login',
                'register': '/api/register',
                'products': '/api/products',
                'reviews': '/api/reviews',
                'salts': '/api/salts',
                'config': '/api/config'
            }
        })
    
    # Register blueprints with new structure
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    app.register_blueprint(salts_bp, url_prefix='/api/salts')
    app.register_blueprint(config_bp, url_prefix='/api/config')
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    debug_mode = config_name == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000, use_reloader=debug_mode)
