# app/budgets/services.py

from app.models.budget import Budget
from app import db
from datetime import datetime

def create_budget(user_id, data):
    budget = Budget(
        user_id=user_id,
        name=data['name'],
        amount=data['amount'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
    )
    db.session.add(budget)
    db.session.commit()
    return budget

def get_user_budgets(user_id):
    return Budget.query.filter_by(user_id=user_id).all()

def update_budget(user_id, budget_id, data):
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if not budget:
        return None

    budget.name = data.get('name', budget.name)
    budget.amount = data.get('amount', budget.amount)
    if 'start_date' in data:
        budget.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    if 'end_date' in data:
        budget.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

    db.session.commit()
    return budget
