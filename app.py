from flask import Flask
from config import Config
from pymongo import MongoClient
from flask_session import Session
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Session initialization - Vercel compatible (Standard Cookies)
# Session(app) is not needed if SESSION_TYPE is None as Flask handles it natively

# Import db just for consistency (already initialized in db.py)
from db import db, mongo_client

# To access the collections globally if needed
users_collection = db['users']
transactions_collection = db['transactions']

# Import blueprints here to avoid circular imports
from routes.auth_routes import auth_bp
from routes.bank_routes import bank_bp

app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
