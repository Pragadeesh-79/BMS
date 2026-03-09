import uuid
from datetime import datetime

class LoanModel:
    def __init__(self, db):
        self.collection = db['loans']

    def request_loan(self, account_number, amount, purpose, payback_period):
        """Creates a new loan request."""
        loan_data = {
            'loan_id': str(uuid.uuid4()),
            'account_number': account_number,
            'amount': float(amount),
            'purpose': purpose,
            'payback_period': payback_period,
            'status': 'Pending',
            'created_at': datetime.utcnow(),
            'due_date': None, # To be set when active
            'interest_rate': 0.05 # Fixed 5% interest
        }
        self.collection.insert_one(loan_data)
        return loan_data

    def get_user_loans(self, account_number):
        """Retrieves all loans for a specific user."""
        return list(self.collection.find({'account_number': account_number}).sort('created_at', -1))

    def get_loan_by_id(self, loan_id):
        return self.collection.find_one({'loan_id': loan_id})

    def approve_loan(self, loan_id, user_model):
        """Mock admin function to simulate approving a loan and depositing the money."""
        loan = self.get_loan_by_id(loan_id)
        if not loan or loan['status'] != 'Pending':
            return False
            
        # Update loan status
        self.collection.update_one(
            {'loan_id': loan_id},
            {'$set': {'status': 'Active', 'due_date': datetime.utcnow()}} # Simplified due date
        )
        
        # Add money to user's balance
        user_model.update_balance(loan['account_number'], loan['amount'])
        return True
