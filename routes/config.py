from flask import Blueprint, request, jsonify
from models import AppConfig

config_bp = Blueprint('config', __name__)

@config_bp.route('/', methods=['GET'])
def get_all_config():
    """Get all app configuration"""
    try:
        configs = AppConfig.query.all()
        config_dict = {}
        for config in configs:
            config_dict[config.key] = config.to_dict()['value']
        
        return jsonify({
            'config': config_dict,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@config_bp.route('/<config_key>', methods=['GET'])
def get_config(config_key):
    """Get specific configuration by key"""
    try:
        config = AppConfig.query.filter_by(key=config_key).first()
        
        if not config:
            return jsonify({'error': 'Configuration not found', 'success': False}), 404
        
        return jsonify({
            'config': config.to_dict(),
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@config_bp.route('/by-category/<category>', methods=['GET'])
def get_config_by_category(category):
    """Get configurations by category (prefix)"""
    try:
        configs = AppConfig.query.filter(AppConfig.key.like(f'{category}.%')).all()
        config_dict = {}
        for config in configs:
            config_dict[config.key] = config.to_dict()['value']
        
        return jsonify({
            'config': config_dict,
            'category': category,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500
