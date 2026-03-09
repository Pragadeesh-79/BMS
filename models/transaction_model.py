import uuid
from datetime import datetime

class TransactionModel:
    def __init__(self, db):
        self.collection = db['transactions']

    def create_transaction(self, sender_account, receiver_account, amount, type, status="completed", description="", session=None):
        """Creates a transaction record."""
        transaction_data = {
            'transaction_id': str(uuid.uuid4()),
            'sender_account': sender_account,
            'receiver_account': receiver_account,
            'amount': float(amount),
            'type': type, # e.g., 'transfer', 'deposit', 'withdrawal'
            'status': status,
            'description': description,
            'timestamp': datetime.utcnow()
        }

        self.collection.insert_one(transaction_data, session=session)
        return transaction_data

    def get_user_transactions(self, account_number, limit=0):
        """Retrieves transactions where the user is either sender or receiver, sorted by newest first."""
        query = {
            '$or': [
                {'sender_account': account_number},
                {'receiver_account': account_number}
            ]
        }
        cursor = self.collection.find(query).sort('timestamp', -1)
        if limit > 0:
            cursor = cursor.limit(limit)
            
        return list(cursor)

    def execute_transfer(self, sender_account, receiver_account, amount, user_model):
        """
        Executes a money transfer.
        This function orchestrates the check-deduct-add flow.
        Note: True transactional atomicity requires MongoDB Replica sets and sessions,
        but for a free tier without transactions set up, we do basic checks.
        """
        amount = float(amount)
        if amount <= 0:
            return {"success": False, "error": "Transfer amount must be positive."}

        sender = user_model.find_by_account_number(sender_account)
        receiver = user_model.find_by_account_number(receiver_account)

        if not sender:
            return {"success": False, "error": "Sender account not found."}
        if not receiver:
            return {"success": False, "error": "Receiver account not found."}

        if sender['balance'] < amount:
            return {"success": False, "error": "Insufficient balance."}

        # Deduct from Sender
        user_model.update_balance(sender_account, -amount)
        # Add to Receiver
        user_model.update_balance(receiver_account, amount)

        # Record the transaction
        txn = self.create_transaction(
            sender_account=sender_account,
            receiver_account=receiver_account,
            amount=amount,
            type='transfer',
            status='completed'
        )

        return {"success": True, "transaction_id": txn['transaction_id']}

    def execute_deposit(self, account_number, amount, user_model):
        """
        Executes a money deposit.
        """
        amount = float(amount)
        if amount <= 0:
            return {"success": False, "error": "Deposit amount must be positive."}

        user = user_model.find_by_account_number(account_number)
        if not user:
            return {"success": False, "error": "Account not found."}

        # Add to Balance
        user_model.update_balance(account_number, amount)

        # Record the transaction
        txn = self.create_transaction(
            sender_account="System",
            receiver_account=account_number,
            amount=amount,
            type='deposit',
            status='completed',
            description="Self Deposit"
        )

        return {"success": True, "transaction_id": txn['transaction_id']}
