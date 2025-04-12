from flask import request, jsonify
from app.models import Account
from app import db

def format_datetime(value):
    return value.strftime('%Y-%m-%d %H:%M:%S') if value else None

def get_all_accounts(user_id):
    try:
        accounts = Account.query.filter_by(user_id=user_id).all()
        if not accounts:
            return jsonify({'message': 'No accounts found'}), 404
        return jsonify([
            {
                'id': acc.id,
                'account_type': acc.account_type,
                'account_number': acc.account_number,
                'balance': float(acc.balance),
                'created_at': format_datetime(acc.created_at),
                'updated_at': format_datetime(acc.updated_at)
            } for acc in accounts
        ]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

def get_account_by_id(user_id, id):
    try:
        account = Account.query.filter_by(id=id, user_id=user_id).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        return jsonify({
            'id': account.id,
            'account_type': account.account_type,
            'account_number': account.account_number,
            'balance': float(account.balance),
            'created_at': format_datetime(account.created_at),
            'updated_at': format_datetime(account.updated_at)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

def create_new_account(user_id):
    try:
        data = request.json
        required_fields = ('account_type', 'account_number')

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        new_account = Account(
            user_id=user_id,
            account_type=data['account_type'],
            account_number=data['account_number'],
            balance=data.get('balance', 0.00)
        )

        db.session.add(new_account)
        db.session.commit()
        return jsonify({'message': 'Account created successfully', 'account_id': new_account.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

def update_existing_account(user_id, id):
    try:
        account = Account.query.filter_by(id=id, user_id=user_id).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        data = request.json

        account.account_type = data.get('account_type', account.account_type)
        account.account_number = data.get('account_number', account.account_number)
        account.balance = data.get('balance', account.balance)

        db.session.commit()
        return jsonify({'message': 'Account updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

def delete_existing_account(user_id, id):
    try:
        account = Account.query.filter_by(id=id, user_id=user_id).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404

        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
