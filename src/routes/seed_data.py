from flask import Blueprint, jsonify
from src.models.user import db, User
from src.models.account import Account, Category
from datetime import datetime, date
from werkzeug.security import generate_password_hash

seed_bp = Blueprint("seed", __name__)

@seed_bp.route("/seed-data", methods=["POST"])
def seed_data():
    """Seed the database with sample data"""
    try:
        # Clear existing data
        Account.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # Create sample users
        users = [
            User(username="seller1", email="seller1@example.com", password_hash=generate_password_hash("password")),
            User(username="seller2", email="seller2@example.com", password_hash=generate_password_hash("password")),
            User(username="buyer1", email="buyer1@example.com", password_hash=generate_password_hash("password"))
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        
        # Create categories
        categories_data = [
            # Main categories
            {"name": "Facebook Accounts", "slug": "facebook-accounts", "parent_id": None},
            {"name": "Instagram Accounts", "slug": "instagram-accounts", "parent_id": None},
            {"name": "Twitter Accounts", "slug": "twitter-accounts", "parent_id": None},
            {"name": "Gmail Accounts", "slug": "gmail-accounts", "parent_id": None},
            {"name": "VKontakte Accounts", "slug": "vkontakte-accounts", "parent_id": None},
        ]
        
        main_categories = {}
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
            db.session.flush()  # Get the ID
            main_categories[cat_data["name"]] = category.id
        
        # Create subcategories
        subcategories_data = [
            # Facebook subcategories
            {"name": "Facebook Softregs", "slug": "facebook-softregs", "parent_id": main_categories["Facebook Accounts"]},
            {"name": "Facebook With friends", "slug": "facebook-with-friends", "parent_id": main_categories["Facebook Accounts"]},
            {"name": "Facebook Aged", "slug": "facebook-aged", "parent_id": main_categories["Facebook Accounts"]},
            {"name": "Facebook For advertising", "slug": "facebook-for-advertising", "parent_id": main_categories["Facebook Accounts"]},
            
            # Instagram subcategories
            {"name": "Instagram Softreg", "slug": "instagram-softreg", "parent_id": main_categories["Instagram Accounts"]},
            {"name": "Instagram Aged", "slug": "instagram-aged", "parent_id": main_categories["Instagram Accounts"]},
            {"name": "Instagram With Followers", "slug": "instagram-with-followers", "parent_id": main_categories["Instagram Accounts"]},
            
            # Twitter subcategories
            {"name": "Twitter Aged", "slug": "twitter-aged", "parent_id": main_categories["Twitter Accounts"]},
            {"name": "Twitter Softreg", "slug": "twitter-softreg", "parent_id": main_categories["Twitter Accounts"]},
            
            # Gmail subcategories
            {"name": "Gmail Softreg", "slug": "gmail-softreg", "parent_id": main_categories["Gmail Accounts"]},
            {"name": "Gmail Aged", "slug": "gmail-aged", "parent_id": main_categories["Gmail Accounts"]},
            
            # VKontakte subcategories
            {"name": "VKontakte Softreg", "slug": "vkontakte-softreg", "parent_id": main_categories["VKontakte Accounts"]},
        ]
        
        subcategories = {}
        for subcat_data in subcategories_data:
            subcategory = Category(**subcat_data)
            db.session.add(subcategory)
            db.session.flush()  # Get the ID
            subcategories[subcat_data["name"]] = subcategory.id
        
        db.session.commit()
        
        # Create sample accounts
        sample_accounts = [
            # Facebook Softregs
            {
                "seller_id": 1,
                "category_id": subcategories["Facebook Softregs"],
                "title": "FB Accounts | Verified by email (email not included). Male or female.",
                "description": "The account profiles may be empty or have limited entries such as photos and other information. 2FA included. Registered from USA IP.",
                "platform": "Facebook",
                "account_type": "Softreg",
                "price": 0.296,
                "stock_quantity": 1691,
                "min_order_quantity": 100,
                "verification_status": "verified_by_email",
                "has_email": False,
                "country": "USA",
                "rating": 4.3,
                "success_rate": 2.7
            },
            {
                "seller_id": 1,
                "category_id": subcategories["Facebook Softregs"],
                "title": "FB Accounts | Verified by e-mail, there is no email in the set.",
                "description": "Male or female. The account profiles may be empty or have limited entries such as photos and other information. 2FA included. Cookies are included.",
                "platform": "Facebook",
                "account_type": "Softreg",
                "price": 0.296,
                "stock_quantity": 1730,
                "min_order_quantity": 100,
                "verification_status": "verified_by_email",
                "has_email": False,
                "rating": 4.6,
                "success_rate": 4.7
            },
            
            # Facebook With friends
            {
                "seller_id": 2,
                "category_id": subcategories["Facebook With friends"],
                "title": "FB Accounts | The number of subscribers is 50+.",
                "description": "Verified by e-mail, there is no email in the set. Male and female. The account profiles may be empty or have limited entries.",
                "platform": "Facebook",
                "account_type": "With friends",
                "price": 0.999,
                "stock_quantity": 41,
                "min_order_quantity": 10,
                "verification_status": "verified_by_email",
                "friends_count": 50,
                "has_email": False,
                "rating": 4.6,
                "success_rate": 0.7
            },
            
            # Instagram Softreg
            {
                "seller_id": 1,
                "category_id": subcategories["Instagram Softreg"],
                "title": "IG Accounts | Email not included. Profile is not filled at all.",
                "description": "2FA in the set. Registered from the USA IP.",
                "platform": "Instagram",
                "account_type": "Softreg",
                "price": 0.185,
                "stock_quantity": 327,
                "min_order_quantity": 100,
                "verification_status": "verified_by_sms",
                "has_email": False,
                "country": "USA",
                "rating": 4.6,
                "success_rate": 4.9
            },
            
            # Instagram With Followers
            {
                "seller_id": 2,
                "category_id": subcategories["Instagram With Followers"],
                "title": "IG Accounts | The account has about 50 followers.",
                "description": "Email address is included in the package(onet.pl, original). A profile picture is added to the account.",
                "platform": "Instagram",
                "account_type": "With Followers",
                "price": 1.11,
                "stock_quantity": 62,
                "min_order_quantity": 100,
                "verification_status": "verified_by_email",
                "followers_count": 50,
                "has_email": True,
                "rating": 4.7,
                "success_rate": 2.5
            }
        ]
        
        for account_data in sample_accounts:
            account = Account(**account_data)
            db.session.add(account)
        
        db.session.commit()
        
        return jsonify({"message": "Database seeded successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


