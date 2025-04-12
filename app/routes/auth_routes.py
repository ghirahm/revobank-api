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

    print(f"[DEBUG] Login attempt: username={username}, password={password}")

    user = User.query.filter_by(username=username).first()

    if not user:
        print("[DEBUG] User not found")
        return jsonify({'error': 'Invalid username or password'}), 401

    print(f"[DEBUG] Stored hash: {user.password_hash}")

    # Use Werkzeug check_password_hash
    is_valid = check_password_hash(user.password_hash, password)

    print(f"[DEBUG] Password valid: {is_valid}")

    if is_valid:
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        print("[DEBUG] Invalid password")
        return jsonify({'error': 'Invalid username or password'}), 401