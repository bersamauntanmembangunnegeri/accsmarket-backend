from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from src.extensions import db
from src.models.user import User
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 409
    
    # Hash password
    password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    new_user = User(
        email=data["email"],
        password_hash=password_hash.decode('utf-8'),
        username=data.get("username", data["email"].split("@")[0]),
        is_admin=data.get("is_admin", False)
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=new_user.id,
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            "message": "User created successfully",
            "access_token": access_token,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "username": new_user.username,
                "is_admin": new_user.is_admin
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to create user"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400
    
    # Find user
    user = User.query.filter_by(email=data["email"]).first()
    
    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=7)
    )
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin
        }
    }), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }), 200

@auth_bp.route("/admin-check", methods=["GET"])
@jwt_required()
def admin_check():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403
    
    return jsonify({"message": "Admin access granted"}), 200

