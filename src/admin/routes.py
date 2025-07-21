from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.account import Account
from src.models.user import User
from src.main import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required():
    """Decorator to check if user is admin"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    return None

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    admin_check = admin_required()
    if admin_check:
        return admin_check
    
    # Get dashboard statistics
    total_accounts = Account.query.count()
    total_users = User.query.count()
    
    return jsonify({
        "message": "Welcome to the Admin Dashboard!",
        "stats": {
            "total_accounts": total_accounts,
            "total_users": total_users
        }
    })

# Product Management (Accounts)
@admin_bp.route("/accounts", methods=["GET"])
@jwt_required()
def get_all_accounts():
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts])

@admin_bp.route("/accounts/<int:account_id>", methods=["GET"])
@jwt_required()
def get_account(account_id):
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    account = Account.query.get_or_404(account_id)
    return jsonify(account.to_dict())

@admin_bp.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    data = request.json
    new_account = Account(
        platform=data["platform"],
        account_type=data["account_type"],
        title=data["title"],
        description=data["description"],
        price=data["price"],
        stock_quantity=data["stock_quantity"],
        rating=data.get("rating"),
        success_rate=data.get("success_rate"),
        min_order_quantity=data.get("min_order_quantity"),
        verification_status=data.get("verification_status"),
        has_email=data.get("has_email"),
        has_phone=data.get("has_phone"),
        country=data.get("country"),
        registration_date=data.get("registration_date"),
        gender=data.get("gender"),
        age_range=data.get("age_range"),
        friends_count=data.get("friends_count"),
        followers_count=data.get("followers_count"),
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.to_dict()), 201

@admin_bp.route("/accounts/<int:account_id>", methods=["PUT"])
@jwt_required()
def update_account(account_id):
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    account = Account.query.get_or_404(account_id)
    data = request.json
    account.platform = data.get("platform", account.platform)
    account.account_type = data.get("account_type", account.account_type)
    account.title = data.get("title", account.title)
    account.description = data.get("description", account.description)
    account.price = data.get("price", account.price)
    account.stock_quantity = data.get("stock_quantity", account.stock_quantity)
    account.rating = data.get("rating", account.rating)
    account.success_rate = data.get("success_rate", account.success_rate)
    account.min_order_quantity = data.get("min_order_quantity", account.min_order_quantity)
    account.verification_status = data.get("verification_status", account.verification_status)
    account.has_email = data.get("has_email", account.has_email)
    account.has_phone = data.get("has_phone", account.has_phone)
    account.country = data.get("country", account.country)
    account.registration_date = data.get("registration_date", account.registration_date)
    account.gender = data.get("gender", account.gender)
    account.age_range = data.get("age_range", account.age_range)
    account.friends_count = data.get("friends_count", account.friends_count)
    account.followers_count = data.get("followers_count", account.followers_count)
    db.session.commit()
    return jsonify(account.to_dict())

@admin_bp.route("/accounts/<int:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id):
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 204

# User Management
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    admin_check = admin_required()
    if admin_check:
        return admin_check
        
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

