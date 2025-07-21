import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from src.extensions import db, jwt
from src.routes.user import user_bp
from src.routes.account import account_bp
from src.routes.seed_data import seed_bp
from src.admin.routes import admin_bp
from src.auth.routes import auth_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf#FGSgvasgf$5$WGT"
app.config["JWT_SECRET_KEY"] = "jwt-secret-string-change-in-production"

# Initialize extensions
db.init_app(app)
jwt.init_app(app)

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(account_bp, url_prefix="/api")
app.register_blueprint(seed_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "AccsMarket API is running",
        "version": "1.0.0"
    })

@app.route("/api")
def api_info():
    return jsonify({
        "message": "AccsMarket API",
        "version": "1.0.0",
        "endpoints": {
            "accounts": "/api/accounts",
            "categories": "/api/categories",
            "accounts_by_category": "/api/accounts/by-category",
            "seed_data": "/api/seed-data"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
