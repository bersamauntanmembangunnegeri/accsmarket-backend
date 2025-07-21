from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.account import Account, Category
from sqlalchemy import or_, and_

account_bp = Blueprint('account', __name__)

@account_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        platform = request.args.get('platform')
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        query = Account.query.filter_by(status='active')
        
        if platform:
            query = query.filter(Account.platform.ilike(f'%{platform}%'))
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(or_(
                Account.title.ilike(f'%{search}%'),
                Account.description.ilike(f'%{search}%')
            ))
        
        if min_price is not None:
            query = query.filter(Account.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Account.price <= max_price)
        
        # Order by featured first, then by created date
        query = query.order_by(Account.is_featured.desc(), Account.created_at.desc())
        
        accounts = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'accounts': [account.to_dict() for account in accounts.items],
            'total': accounts.total,
            'pages': accounts.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@account_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Get a specific account by ID"""
    try:
        account = Account.query.get_or_404(account_id)
        return jsonify(account.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    """Create a new account listing"""
    try:
        data = request.get_json()
        
        account = Account(
            seller_id=data.get('seller_id'),
            category_id=data.get('category_id'),
            title=data.get('title'),
            description=data.get('description'),
            platform=data.get('platform'),
            account_type=data.get('account_type'),
            price=data.get('price'),
            stock_quantity=data.get('stock_quantity', 1),
            min_order_quantity=data.get('min_order_quantity', 1),
            verification_status=data.get('verification_status'),
            friends_count=data.get('friends_count'),
            followers_count=data.get('followers_count'),
            has_email=data.get('has_email', False),
            has_phone=data.get('has_phone', False),
            country=data.get('country'),
            gender=data.get('gender'),
            age_range=data.get('age_range'),
            rating=data.get('rating', 0),
            success_rate=data.get('success_rate', 0)
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify(account.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@account_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify([category.to_dict() for category in categories])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@account_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        category = Category(
            name=data.get('name'),
            slug=data.get('slug'),
            description=data.get('description'),
            parent_id=data.get('parent_id')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify(category.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@account_bp.route('/accounts/by-category', methods=['GET'])
def get_accounts_by_category():
    """Get accounts grouped by category and subcategory"""
    try:
        # Get all main categories
        main_categories = Category.query.filter_by(parent_id=None, is_active=True).all()
        result = {}
        
        for main_category in main_categories:
            result[main_category.name] = {}
            
            # Get subcategories
            subcategories = Category.query.filter_by(parent_id=main_category.id, is_active=True).all()
            
            for subcategory in subcategories:
                # Get accounts for this subcategory (limit to 5 for homepage display)
                accounts = Account.query.filter_by(
                    category_id=subcategory.id, 
                    status='active'
                ).order_by(Account.is_featured.desc(), Account.created_at.desc()).limit(5).all()
                
                if accounts:  # Only include subcategories that have accounts
                    result[main_category.name][subcategory.name] = [account.to_dict() for account in accounts]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

