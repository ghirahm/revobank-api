from flask import Blueprint, request, jsonify
from app.models import User
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@user_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        user = User.query.first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'username': user.username, 'email': user.email}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@user_bp.route('/me', methods=['PUT'])
def update_user():
    try:
        data = request.json
        user = User.query.first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500
