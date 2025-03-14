from flask import Blueprint, request, jsonify
from app.models import Transaction
from app import db

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    try:
        transactions = Transaction.query.all()
        if not transactions:
            return jsonify({'message': 'No transactions found'}), 404
        return jsonify([{'type': tx.type, 'amount': tx.amount} for tx in transactions]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@transaction_bp.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    try:
        transaction = Transaction.query.get_or_404(id)
        return jsonify({'type': transaction.type, 'amount': transaction.amount}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    try:
        data = request.json

        if not all(k in data for k in ('account_id', 'type', 'amount')):
            return jsonify({'error': 'Missing required fields'}), 400

        if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
            return jsonify({'error': 'Invalid amount, must be a positive number'}), 400

        new_transaction = Transaction(
            account_id=data['account_id'],
            type=data['type'],
            amount=data['amount']
        )

        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
