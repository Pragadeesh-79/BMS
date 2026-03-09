import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

# Global db object initialized as None
_db = None

def get_db():
    global _db
    if _db is None:
        if not MONGO_URI:
            print("CRITICAL: MONGO_URI is missing!")
            # Fallback to local only for local devs, but on Vercel this will likely fail
            client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000)
            _db = client['banking_db']
        else:
            print("Initializing MongoDB Atlas connection...")
            client = MongoClient(MONGO_URI, connectTimeoutMS=5000, socketTimeoutMS=5000)
            _db = client.get_database() 
    return _db
