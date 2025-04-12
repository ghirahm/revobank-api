from app import db
from app.models.bill import Bill
from datetime import datetime

def create_bill(user_id, data):
    bill = Bill(
        user_id=user_id,
        biller_name=data['biller_name'],
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
        amount=data['amount'],
        account_id=data['account_id']
    )
    db.session.add(bill)
    db.session.commit()
    return bill

def get_user_bills(user_id):
    return Bill.query.filter_by(user_id=user_id).all()

def update_bill(user_id, bill_id, data):
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    if not bill:
        return None
    bill.biller_name = data.get('biller_name', bill.biller_name)
    bill.amount = data.get('amount', bill.amount)
    bill.account_id = data.get('account_id', bill.account_id)
    if 'due_date' in data:
        bill.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    db.session.commit()
    return bill

def delete_bill(user_id, bill_id):
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    if not bill:
        return False
    db.session.delete(bill)
    db.session.commit()
    return True
