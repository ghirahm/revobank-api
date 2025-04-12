from flask import Blueprint, jsonify
from app.services.transaction_category_service import get_transaction_categories

transaction_category_bp = Blueprint('transactions', __name__)

# Read Transaction Category Data
@transaction_category_bp.route('/category', methods=['GET'])
def list_categories():
    categories = get_transaction_categories()
    return jsonify([{'id': cat.id, 'name': cat.name} for cat in categories])
