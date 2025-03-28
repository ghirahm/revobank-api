from app.models import Transaction, Account
from app import db

def get_all_transactions():
    transactions = Transaction.query.all()
    if not transactions:
        return {'message': 'No transactions found'}, 404
    return [
        {
            'id': tx.id,
            'type': tx.type,
            'amount': float(tx.amount),
            'from_account_id': tx.from_account_id,
            'to_account_id': tx.to_account_id,
            'description': tx.description,
            'created_at': tx.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for tx in transactions
    ], 200

def get_transaction_by_id(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return {
        'id': transaction.id,
        'type': transaction.type,
        'amount': float(transaction.amount),
        'from_account_id': transaction.from_account_id,
        'to_account_id': transaction.to_account_id,
        'description': transaction.description,
        'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }, 200

def create_transaction(data):
    required_fields = ('type', 'amount')
    if not all(k in data for k in required_fields):
        return {'error': 'Missing required fields'}, 400

    transaction_type = data['type'].lower()
    amount = data['amount']

    if transaction_type not in ['deposit', 'withdrawal', 'transfer']:
        return {'error': 'Invalid transaction type'}, 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return {'error': 'Amount must be a positive number'}, 400

    from_account = None
    to_account = None

    try:
        if transaction_type == 'deposit':
            if 'to_account_id' not in data:
                return {'error': 'Missing to_account_id for deposit'}, 400
            to_account = Account.query.get(data['to_account_id'])
            if not to_account:
                return {'error': 'Recipient account not found'}, 404
            to_account.balance += amount

        elif transaction_type == 'withdrawal':
            if 'from_account_id' not in data:
                return {'error': 'Missing from_account_id for withdrawal'}, 400
            from_account = Account.query.get(data['from_account_id'])
            if not from_account:
                return {'error': 'Sender account not found'}, 404
            if from_account.balance < amount:
                return {'error': 'Insufficient balance'}, 400
            from_account.balance -= amount

        elif transaction_type == 'transfer':
            if 'from_account_id' not in data or 'to_account_id' not in data:
                return {'error': 'Both from_account_id and to_account_id are required for transfer'}, 400
            from_account = Account.query.get(data['from_account_id'])
            to_account = Account.query.get(data['to_account_id'])
            if not from_account or not to_account:
                return {'error': 'One or both accounts not found'}, 404
            if from_account.balance < amount:
                return {'error': 'Insufficient balance for transfer'}, 400
            from_account.balance -= amount
            to_account.balance += amount

        new_transaction = Transaction(
            from_account_id=data.get('from_account_id'),
            to_account_id=data.get('to_account_id'),
            amount=amount,
            type=transaction_type,
            description=data.get('description', '')
        )

        db.session.add(new_transaction)
        db.session.commit()
        return {'message': 'Transaction created successfully', 'transaction_id': new_transaction.id}, 201

    except Exception as e:
        db.session.rollback()
        return {'error': 'Internal Server Error', 'details': str(e)}, 500

def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)

        if transaction.type == 'deposit' and transaction.to_account:
            transaction.to_account.balance -= transaction.amount
        elif transaction.type == 'withdrawal' and transaction.from_account:
            transaction.from_account.balance += transaction.amount
        elif transaction.type == 'transfer' and transaction.from_account and transaction.to_account:
            transaction.from_account.balance += transaction.amount
            transaction.to_account.balance -= transaction.amount

        db.session.delete(transaction)
        db.session.commit()
        return {'message': 'Transaction deleted successfully'}, 200

    except Exception as e:
        db.session.rollback()
        return {'error': 'Internal Server Error', 'details': str(e)}, 500
