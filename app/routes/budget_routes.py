# app/budgets/routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.budget_service import create_budget, get_user_budgets, update_budget

budgets_bp = Blueprint('budgets', __name__)

# Create Budget Data
@budgets_bp.route('/', methods=['POST'])
@jwt_required()
def post_budget():
    user_id = get_jwt_identity()
    data = request.get_json()
    budget = create_budget(user_id, data)
    return jsonify({'message': 'Budget created', 'budget_id': budget.id}), 201

# Read Budget Data
@budgets_bp.route('/', methods=['GET'])
@jwt_required()
def list_budgets():
    user_id = get_jwt_identity()
    budgets = get_user_budgets(user_id)
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'amount': b.amount,
        'start_date': b.start_date.isoformat(),
        'end_date': b.end_date.isoformat()
    } for b in budgets])

# Update Budget Data
@budgets_bp.route('/<int:budget_id>', methods=['PUT'])
@jwt_required()
def put_budget(budget_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    budget = update_budget(user_id, budget_id, data)
    if not budget:
        return jsonify({'error': 'Budget not found'}), 404
    return jsonify({'message': 'Budget updated'})
