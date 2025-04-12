from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # print(f"[AUTH DEBUG] Login attempt: username={username}, password={password}")
    user = User.query.filter_by(username=username).first()

    if not user:
        # print("[AUTH DEBUG] User lookup failed during login attempt.")
        return jsonify({'error': 'Authentication failed. Please check your credentials.'}), 401

    # print(f"[AUTH DEBUG] Stored hash: {user.password_hash}")
    is_valid = check_password_hash(user.password_hash, password)

    # print(f"[AUTH DEBUG] Password valid: {is_valid}")

    if is_valid:
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Authentication successful', 'access_token': access_token}), 200
    else:
        # print(f"[LOGIN ATTEMPT] Failed login for user ID: {user.id} due to invalid credentials.")
        return jsonify({'error': 'Authentication failed. Please check your credentials.'}), 401
