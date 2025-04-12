from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.account_service import (
    get_all_accounts,
    get_account_by_id,
    create_new_account,
    update_existing_account,
    delete_existing_account
)

account_bp = Blueprint('account', __name__)

# Read Account Data
@account_bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    return get_all_accounts(user_id)

# Read Account Data (Based on ID)
@account_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_account(id):
    user_id = get_jwt_identity()
    return get_account_by_id(user_id, id)

# Create Account Data
@account_bp.route('/', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    return create_new_account(user_id)

# Update Account Data
@account_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_account(id):
    user_id = get_jwt_identity()
    return update_existing_account(user_id, id)

# Delete Account Data
@account_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_account(id):
    user_id = get_jwt_identity()
    return delete_existing_account(user_id, id)