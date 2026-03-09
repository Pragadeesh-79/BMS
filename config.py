import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Session / Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-default'
    SESSION_TYPE = 'filesystem'
    
    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # SMTP Settings
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
