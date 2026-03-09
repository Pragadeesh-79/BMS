from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
from models.transaction_model import TransactionModel
from models.loan_model import LoanModel
from utils.decorators import login_required
from utils.email_service import send_transaction_email

bank_bp = Blueprint('bank', __name__)

from db import db
user_model = UserModel(db)
transaction_model = TransactionModel(db)
loan_model = LoanModel(db)

@bank_bp.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('bank.dashboard'))
    return render_template('splash.html')

@bank_bp.route('/dashboard')
@login_required
def dashboard():
    account_number = session.get('account_number')
    user = user_model.find_by_account_number(account_number)
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
        
    recent_transactions = transaction_model.get_user_transactions(account_number, limit=5)
    
    return render_template('dashboard.html', user=user, transactions=recent_transactions)

@bank_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'GET':
        account_number = session.get('account_number')
        user = user_model.find_by_account_number(account_number)
        return render_template('transfer.html', user=user)
        
    sender_account = session.get('account_number')
    receiver_account = request.form.get('receiver_account')
    amount = request.form.get('amount')
    description = request.form.get('description', '')

    if not receiver_account or not amount:
        flash('Receiver account and amount are required.', 'error')
        return redirect(url_for('bank.transfer'))

    if sender_account == receiver_account:
        flash('You cannot transfer money to yourself.', 'error')
        return redirect(url_for('bank.transfer'))

    try:
        amount = float(amount)
    except ValueError:
        flash('Invalid amount format.', 'error')
        return redirect(url_for('bank.transfer'))

    result = transaction_model.execute_transfer(
        sender_account, 
        receiver_account, 
        amount, 
        user_model
    )

    if result['success']:
        # Fetch updated balances to send emails
        sender = user_model.find_by_account_number(sender_account)
        receiver = user_model.find_by_account_number(receiver_account)
        
        # Send emails
        send_transaction_email(
            sender['email'], 'debit', amount, receiver_account, sender['balance']
        )
        send_transaction_email(
            receiver['email'], 'credit', amount, sender_account, receiver['balance']
        )
        
        flash('Transfer successful!', 'success')
        return redirect(url_for('bank.dashboard'))
    else:
        flash(result['error'], 'error')
        return redirect(url_for('bank.transfer'))

@bank_bp.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    account_number = session.get('account_number')
    user = user_model.find_by_account_number(account_number)
    
    if request.method == 'GET':
        return render_template('deposit.html', user=user)
        
    amount = request.form.get('amount')
    
    if not amount:
        flash('Amount is required.', 'error')
        return redirect(url_for('bank.deposit'))

    try:
        amount = float(amount)
    except ValueError:
        flash('Invalid amount format.', 'error')
        return redirect(url_for('bank.deposit'))

    result = transaction_model.execute_deposit(
        account_number, 
        amount, 
        user_model
    )

    if result['success']:
        flash('Deposit successful!', 'success')
        return redirect(url_for('bank.dashboard'))
    else:
        flash(result['error'], 'error')
        return redirect(url_for('bank.deposit'))

@bank_bp.route('/transactions')
@login_required
def transactions():
    account_number = session.get('account_number')
    user = user_model.find_by_account_number(account_number)
    all_transactions = transaction_model.get_user_transactions(account_number)
    
    return render_template('transactions.html', user=user, transactions=all_transactions)

@bank_bp.route('/loans', methods=['GET', 'POST'])
@login_required
def loans():
    account_number = session.get('account_number')
    user = user_model.find_by_account_number(account_number)
    
    if request.method == 'POST':
        amount = request.form.get('amount')
        purpose = request.form.get('purpose')
        payback_period = request.form.get('payback_period')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Loan amount must be greater than zero.', 'error')
                return redirect(url_for('bank.loans'))
        except ValueError:
            flash('Invalid amount format.', 'error')
            return redirect(url_for('bank.loans'))
            
        loan = loan_model.request_loan(account_number, amount, purpose, payback_period)
        
        # Approve loan automatically as requested
        loan_model.approve_loan(loan['loan_id'], user_model)
        
        # Record it as a deposit for history without updating balance twice
        transaction_model.create_transaction(
            sender_account="Lending System",
            receiver_account=account_number,
            amount=amount,
            type='deposit',
            description=f"Loan Approved: {purpose}"
        )
        
        flash('Loan requested and approved automatically.', 'success')
        return redirect(url_for('bank.loans'))
        
    user_loans = loan_model.get_user_loans(account_number)
    
    return render_template('loans.html', user=user, loans=user_loans)

