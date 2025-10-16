from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    avg_rating = db.Column(db.Float, default=0.0)
    chemical_form = db.Column(db.String(200))
    image_url = db.Column(db.Text)
    generic_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    # Additional fields for complete product information
    description = db.Column(db.Text)
    dosage = db.Column(db.String(100))
    pack_size = db.Column(db.String(50))
    prescription_required = db.Column(db.Boolean, default=False)
    uses = db.Column(db.Text)  # JSON string of array
    side_effects = db.Column(db.Text)  # JSON string of array
    how_it_works = db.Column(db.Text)
    faq_content = db.Column(db.Text)  # JSON string of FAQ data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    salts = db.relationship('Salt', backref='product', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    descriptions = db.relationship('Description', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_relations=False):
        import json
        result = {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'avg_rating': self.avg_rating,
            'chemical_form': self.chemical_form,
            'image_url': self.image_url,
            'generic_name': self.generic_name,
            'category': self.category,
            'description': self.description,
            'dosage': self.dosage,
            'pack_size': self.pack_size,
            'prescription_required': self.prescription_required,
            'uses': json.loads(self.uses) if self.uses else [],
            'side_effects': json.loads(self.side_effects) if self.side_effects else [],
            'how_it_works': self.how_it_works,
            'faq_content': json.loads(self.faq_content) if self.faq_content else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            result['salts'] = [salt.to_dict() for salt in self.salts]
            result['reviews'] = [review.to_dict() for review in self.reviews]
            result['descriptions'] = [desc.to_dict() for desc in self.descriptions]
        
        return result

class Salt(db.Model):
    __tablename__ = 'salts'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    salt_name = db.Column(db.String(100), nullable=False)
    strength = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'salt_name': self.salt_name,
            'strength': self.strength,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_name': self.user_name,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Description(db.Model):
    __tablename__ = 'descriptions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # about, how_it_works, side_effects, faq
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
