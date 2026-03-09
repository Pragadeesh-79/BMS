from flask import Flask, jsonify
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print("!!! SERVER ERROR DETECTED !!!")
    error_trace = traceback.format_exc()
    print(error_trace)
    # Return limited traceback for debugging on Vercel
    return f"Internal Server Error: {str(e)}\n\n{error_trace[:500]}", 500

# Standard Flask Cookie Session (No filesystem needed for Vercel)

# Import and Register blueprints
from routes.auth_routes import auth_bp
from routes.bank_routes import bank_bp

app.register_blueprint(auth_bp)
app.register_blueprint(bank_bp)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
