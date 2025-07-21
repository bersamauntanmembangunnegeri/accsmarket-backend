from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    parent = db.relationship('Category', remote_side=[id], backref='subcategories')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    platform = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=1)
    min_order_quantity = db.Column(db.Integer, default=1)
    
    # Account specifications
    verification_status = db.Column(db.String(50))
    registration_date = db.Column(db.Date)
    friends_count = db.Column(db.Integer)
    followers_count = db.Column(db.Integer)
    has_email = db.Column(db.Boolean, default=False)
    has_phone = db.Column(db.Boolean, default=False)
    country = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    age_range = db.Column(db.String(20))
    
    # Seller ratings and stats
    rating = db.Column(db.Numeric(3, 2), default=0.00)
    success_rate = db.Column(db.Numeric(5, 2), default=0.00)
    total_sales = db.Column(db.Integer, default=0)
    
    # Status and timestamps
    status = db.Column(db.String(20), default='active')
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    seller = db.relationship('User', backref='accounts')
    category = db.relationship('Category', backref='accounts')
    
    def __repr__(self):
        return f'<Account {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description,
            'platform': self.platform,
            'account_type': self.account_type,
            'price': float(self.price) if self.price else 0,
            'stock_quantity': self.stock_quantity,
            'min_order_quantity': self.min_order_quantity,
            'verification_status': self.verification_status,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'friends_count': self.friends_count,
            'followers_count': self.followers_count,
            'has_email': self.has_email,
            'has_phone': self.has_phone,
            'country': self.country,
            'gender': self.gender,
            'age_range': self.age_range,
            'rating': float(self.rating) if self.rating else 0,
            'success_rate': float(self.success_rate) if self.success_rate else 0,
            'total_sales': self.total_sales,
            'status': self.status,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'category': self.category.to_dict() if self.category else None
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    delivery_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='purchases')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    account = db.relationship('Account', backref='orders')
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'account_id': self.account_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'delivery_details': self.delivery_details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

