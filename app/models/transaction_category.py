from app import db

class TransactionCategory(db.Model):
    # Primary key for the transaction category
    id = db.Column(db.Integer, primary_key=True)

    # Name of the category (e.g., "Food", "Rent", "Salary")
    # This field is unique, so no two categories can have the same name
    name = db.Column(db.String(100), nullable=False, unique=True)
