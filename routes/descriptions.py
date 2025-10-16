from flask import Blueprint, request, jsonify
from models import Description

descriptions_bp = Blueprint('descriptions', __name__)

@descriptions_bp.route('/', methods=['GET'])
def get_descriptions():
    """
    GET /api/description - Get product details/descriptions
    """
    try:
        product_id = request.args.get('product_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        description_type = request.args.get('type')  # about, how_it_works, side_effects, faq
        
        query = Description.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        if description_type:
            query = query.filter_by(type=description_type)
        
        descriptions = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'descriptions': [desc.to_dict() for desc in descriptions.items],
            'total': descriptions.total,
            'pages': descriptions.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': descriptions.has_next,
            'has_prev': descriptions.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@descriptions_bp.route('/<description_id>', methods=['GET'])
def get_description(description_id):
    """
    GET /api/description/{id} - Get specific product description
    """
    try:
        description = Description.query.get(description_id)
        
        if not description:
            return jsonify({'error': 'Description not found'}), 404
        
        return jsonify({
            'description': description.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
