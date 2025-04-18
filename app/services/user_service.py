from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

def create_user(data):
    required_fields = ('username', 'email', 'password')

    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully', 'user_id': new_user.id}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': 'Failed to create user', 'details': str(e)}, 500

def get_user(id, user_id):
    # Ensure that the current user can only access their own data

    print (user_id)
    if int(user_id) != id:
        return {'error': 'Unauthorized access to this user\'s data'}, 403

    user = User.query.get_or_404(id)
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }, 200

def update_user(id, user_id, data):
    # Ensure that the current user can only update their own data
    if int(user_id) != id:
        return {'error': 'Unauthorized access to update this user\'s data'}, 403

    user = User.query.get_or_404(id)

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return {'message': 'User updated successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'Failed to update user', 'details': str(e)}, 500

def delete_user(id, user_id):
    # Ensure that the current user can only delete their own data
    if int(user_id) != id:
        return {"error": "Unauthorized access to delete this user"}, 403

    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete user", "details": str(e)}, 500