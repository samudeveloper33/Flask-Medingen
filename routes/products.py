from flask import Blueprint, request, jsonify
from models import Product
from sqlalchemy import or_

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    """
    GET /api/products - Fetch medicine list with price, etc.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        brand = request.args.get('brand', '')
        category = request.args.get('category', '')
        generic_name = request.args.get('generic_name', '')
        exclude_id = request.args.get('exclude_id')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        query = Product.query
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.generic_name.ilike(f'%{search}%'),
                    Product.brand.ilike(f'%{search}%')
                )
            )
        
        if brand:
            query = query.filter(Product.brand.ilike(f'%{brand}%'))
        
        if category:
            query = query.filter(Product.category.ilike(f'%{category}%'))
        
        if generic_name:
            query = query.filter(Product.generic_name.ilike(f'%{generic_name}%'))
        
        if exclude_id:
            query = query.filter(Product.id != exclude_id)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Paginate results
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': products.has_next,
            'has_prev': products.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/{id} - Get specific product details
    """
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({
            'product': product.to_dict(include_relations=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
