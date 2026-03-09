import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

try:
    if MONGO_URI:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Verify connection
        mongo_client.admin.command('ping')
        db = mongo_client.get_database() # Gets default database from URI
        print("Successfully connected to MongoDB Atlas.")
    else:
        raise ValueError("MONGO_URI is empty")
except Exception as e:
    print(f"Error connecting to MongoDB Atlas: {e}")
    # Fallback to local db for development purposes to avoid instant crash if not set
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client['banking_db']
    print("Falling back to local MongoDB mongodb://localhost:27017/banking_db")
