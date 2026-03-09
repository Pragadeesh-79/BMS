from flask import Flask, jsonify
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Standard Flask Cookie Session (No filesystem needed for Vercel)

# Import db and models
from db import db
from routes.auth_routes import auth_bp
from routes.bank_routes import bank_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Vercel requires the app object to be available at the top level
# which it is here as 'app'.

if __name__ == '__main__':
    app.run(debug=True, port=5000)
