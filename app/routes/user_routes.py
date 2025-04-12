from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from app.services.user_service import (
    create_user, 
    get_user, 
    update_user, 
    delete_user
)

user_bp = Blueprint('user', __name__)

# User Registration
@user_bp.route('/register', methods=['POST'])
def create_user_route():
    try:
        data = request.json
        response, status = create_user(data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# Read User Data (Based on ID)
@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user_route(id):
    try:
        response, status = get_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# Update User Data (Based on ID)
@user_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user_route(id):
    try:
        data = request.json
        response, status = update_user(id, data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# Delete User Data (Based on ID)
@user_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(id):
    try:
        response, status = delete_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
