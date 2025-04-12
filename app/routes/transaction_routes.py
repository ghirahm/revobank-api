from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from app.services.transaction_service import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    delete_transaction
)

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    try:
        transactions = get_all_transactions()
        if transactions is None:
            return jsonify({'message': 'No transactions found'}), 404
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@transaction_bp.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    try:
        transaction = get_transaction_by_id(id)
        return jsonify(transaction), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@transaction_bp.route('/', methods=['POST'])
def create_transaction_route():
    try:
        data = request.json
        response, status = create_transaction(data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@transaction_bp.route('/<int:id>', methods=['DELETE'])
def delete_transaction_route(id):
    try:
        response, status = delete_transaction(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
