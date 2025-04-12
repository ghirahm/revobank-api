from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.bill_service import create_bill, get_user_bills, update_bill, delete_bill

bill_bp = Blueprint('bills', __name__)

@bill_bp.route('/', methods=['POST'])
@jwt_required()
def post_bill():
    user_id = get_jwt_identity()
    data = request.get_json()
    bill = create_bill(user_id, data)
    return jsonify({'message': 'Bill scheduled', 'bill_id': bill.id}), 201

@bill_bp.route('/', methods=['GET'])
@jwt_required()
def list_bills():
    user_id = get_jwt_identity()
    bills = get_user_bills(user_id)
    return jsonify([{
        'id': b.id,
        'biller_name': b.biller_name,
        'due_date': b.due_date.isoformat(),
        'amount': b.amount,
        'account_id': b.account_id
    } for b in bills])

@bill_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def put_bill(bill_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    bill = update_bill(user_id, bill_id, data)
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404
    return jsonify({'message': 'Bill updated'})

@bill_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill_route(bill_id):
    user_id = get_jwt_identity()
    success = delete_bill(user_id, bill_id)
    if not success:
        return jsonify({'error': 'Bill not found'}), 404
    return jsonify({'message': 'Bill cancelled'})
