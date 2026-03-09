import bcrypt
import random
from datetime import datetime

class UserModel:
    def __init__(self, db):
        self.collection = db['users']

    def generate_account_number(self):
        """Generates a unique 10-digit account number."""
        while True:
            # Generate a 10-digit string
            acct_num = str(random.randint(1000000000, 9999999999))
            if not self.collection.find_one({'account_number': acct_num}):
                return acct_num

    def create_user(self, name, email, phone, password):
        """Creates a new user with a hashed password and unique account number."""
        if self.find_by_email(email):
            return {"success": False, "error": "Email already exists."}

        # Hash the password
        # bcrypt.hashpw requires bytes, so we encode the password to UTF-8
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        account_number = self.generate_account_number()

        user_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'password_hash': hashed_password,
            'account_number': account_number,
            'balance': 1000.0,
            'created_at': datetime.utcnow()
        }

        self.collection.insert_one(user_data)
        return {"success": True, "account_number": account_number}

    def find_by_email(self, email):
        return self.collection.find_one({'email': email})

    def find_by_account_number(self, account_number):
        return self.collection.find_one({'account_number': account_number})

    def verify_password(self, email, password):
        """Verifies a user's password."""
        user = self.find_by_email(email)
        if not user or 'password_hash' not in user:
            return False
            
        password_bytes = password.encode('utf-8')
        hashed = user['password_hash']
        
        # Handle cases where the hash might be stored as a string or binary
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
            
        try:
            return bcrypt.checkpw(password_bytes, hashed)
        except Exception as e:
            print(f"Password verification error: {e}")
            return False

    def update_balance(self, account_number, amount, session=None):
        """Updates the balance by adding amount. amount can be negative for deduction.
        If using a replica set, passing the 'session' allows for transactions."""
        return self.collection.update_one(
            {'account_number': account_number},
            {'$inc': {'balance': amount}},
            session=session
        )
