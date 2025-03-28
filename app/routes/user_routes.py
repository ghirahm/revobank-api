from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def create_user_route():
    try:
        data = request.json
        response, status = create_user(data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@user_bp.route('/<int:id>', methods=['GET'])
def get_user_route(id):
    try:
        response, status = get_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user_route(id):
    try:
        data = request.json
        response, status = update_user(id, data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user_route(id):
    try:
        response, status = delete_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
