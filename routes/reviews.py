from flask import Blueprint, request, jsonify
from models import Review, Product
from sqlalchemy import func

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    """
    GET /api/reviews - Get product reviews
    """
    try:
        product_id = request.args.get('product_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Review.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        reviews = query.order_by(Review.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews.items],
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': reviews.has_next,
            'has_prev': reviews.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    GET /api/reviews/{id} - Get specific review
    """
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify({
            'review': review.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/stats/<product_id>', methods=['GET'])
def get_review_stats(product_id):
    """
    GET /api/reviews/stats/{product_id} - Get review statistics for a product
    """
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get rating distribution
        rating_stats = Review.query.with_entities(
            Review.rating,
            func.count(Review.rating).label('count')
        ).filter_by(product_id=product_id).group_by(Review.rating).all()
        
        total_reviews = sum(stat.count for stat in rating_stats)
        avg_rating = product.avg_rating
        
        rating_distribution = {i: 0 for i in range(1, 6)}
        for stat in rating_stats:
            rating_distribution[stat.rating] = stat.count
        
        return jsonify({
            'product_id': product_id,
            'total_reviews': total_reviews,
            'average_rating': avg_rating,
            'rating_distribution': rating_distribution
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
