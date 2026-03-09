import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Global db object initialized as None
_db = None

def get_db():
    global _db
    if _db is None:
        # Read from environment at runtime
        mongo_uri = os.environ.get('MONGO_URI')
        
        if not mongo_uri:
            # Check for MONGODB_URI as a common alternative
            mongo_uri = os.environ.get('MONGODB_URI')
            
        if not mongo_uri:
            raise RuntimeError(
                "CRITICAL ERROR: 'MONGO_URI' environment variable is missing. "
                "Please add it in your Vercel Project Settings -> Environment Variables."
            )
            
        print("Initializing MongoDB Atlas connection...")
        try:
            client = MongoClient(mongo_uri, connectTimeoutMS=10000, socketTimeoutMS=10000)
            # Use the default database from the connection string if possible
            _db = client.get_database()
            print("MongoDB Atlas connection established.")
        except Exception as e:
            raise RuntimeError(f"CRITICAL ERROR: Failed to connect to MongoDB Atlas: {str(e)}")
            
    return _db
