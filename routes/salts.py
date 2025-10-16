from flask import Blueprint, request, jsonify
from models import Salt

salts_bp = Blueprint('salts', __name__)

@salts_bp.route('/', methods=['GET'])
def get_salts():
    """
    GET /api/salts - Get tablet salt content
    """
    try:
        product_id = request.args.get('product_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Salt.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        salts = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'salts': [salt.to_dict() for salt in salts.items],
            'total': salts.total,
            'pages': salts.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': salts.has_next,
            'has_prev': salts.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@salts_bp.route('/<salt_id>', methods=['GET'])
def get_salt(salt_id):
    """
    GET /api/salts/{id} - Get specific salt information
    """
    try:
        salt = Salt.query.get(salt_id)
        
        if not salt:
            return jsonify({'error': 'Salt not found'}), 404
        
        return jsonify({
            'salt': salt.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
