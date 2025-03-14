from flask import Blueprint, request, jsonify
from app.models import Account
from app import db

account_bp = Blueprint('account', __name__)

@account_bp.route('/', methods=['GET'])
def get_accounts():
    try:
        accounts = Account.query.all()
        if not accounts:
            return jsonify({'message': 'No accounts found'}), 404
        return jsonify([{'account_number': acc.account_number, 'balance': acc.balance} for acc in accounts]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@account_bp.route('/<int:id>', methods=['GET'])
def get_account(id):
    try:
        account = Account.query.get_or_404(id)
        return jsonify({'account_number': account.account_number, 'balance': account.balance}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@account_bp.route('/', methods=['POST'])
def create_account():
    try:
        data = request.json
        if not all(k in data for k in ('user_id', 'account_number')):
            return jsonify({'error': 'Missing required fields'}), 400

        new_account = Account(
            user_id=data['user_id'],
            account_number=data['account_number'],
            balance=data.get('balance', 0.0)
        )
        db.session.add(new_account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@account_bp.route('/<int:id>', methods=['PUT'])
def update_account(id):
    try:
        account = Account.query.get_or_404(id)
        data = request.json

        # Update hanya jika field ada di request
        account.account_number = data.get('account_number', account.account_number)
        account.balance = data.get('balance', account.balance)

        db.session.commit()
        return jsonify({'message': 'Account updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@account_bp.route('/<int:id>', methods=['DELETE'])
def delete_account(id):
    try:
        account = Account.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500