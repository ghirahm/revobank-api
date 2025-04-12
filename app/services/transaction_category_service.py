from app.models.transaction_category import TransactionCategory

def get_transaction_categories():
    return TransactionCategory.query.all()