import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

try:
    if MONGO_URI:
        # Use a more resilient client initialization without blocking pings on import
        mongo_client = MongoClient(MONGO_URI, connectTimeoutMS=5000, socketTimeoutMS=5000)
        db = mongo_client.get_database()
        print("MongoDB Atlas client initialized.")
    else:
        raise ValueError("MONGO_URI environment variable is missing.")
except Exception as e:
    print(f"MongoDB Initialization Warning: {e}")
    # Fallback to local only as absolute last resort
    mongo_client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    db = mongo_client['banking_db']
