from flask import Blueprint, request, jsonify
from app.services.account_service import (
    get_all_accounts,
    get_account_by_id,
    create_new_account,
    update_existing_account,
    delete_existing_account
)

account_bp = Blueprint('account', __name__)

@account_bp.route('/', methods=['GET'])
def get_accounts():
    return get_all_accounts()

@account_bp.route('/<int:id>', methods=['GET'])
def get_account(id):
    return get_account_by_id(id)

@account_bp.route('/', methods=['POST'])
def create_account():
    return create_new_account()

@account_bp.route('/<int:id>', methods=['PUT'])
def update_account(id):
    return update_existing_account(id)

@account_bp.route('/<int:id>', methods=['DELETE'])
def delete_account(id):
    return delete_existing_account(id)
