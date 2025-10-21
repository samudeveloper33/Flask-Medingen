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


class AppConfig(db.Model):
    """Store dynamic configuration for the app like trust indicators, disclaimer, etc."""
    __tablename__ = 'app_config'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)  # JSON string for complex values
    type = db.Column(db.String(50), default='string')  # string, json, number, boolean
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        import json
        value = self.value
        if self.type == 'json':
            try:
                value = json.loads(self.value)
            except:
                value = self.value
        elif self.type == 'number':
            try:
                value = float(self.value)
            except:
                value = self.value
        elif self.type == 'boolean':
            value = self.value.lower() in ('true', '1', 'yes')
            
        return {
            'id': self.id,
            'key': self.key,
            'value': value,
            'type': self.type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
