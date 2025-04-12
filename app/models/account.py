from datetime import datetime
from app import db

class Account(db.Model):
    # __tablename__ = 'account'

    # Primary key for the Account model
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the User model (one user can have many accounts)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_account_user_id'),
        nullable=False
    )

    # Type of account (e.g., savings, checking, credit, etc.)
    account_type = db.Column(db.String(50), nullable=False)

    # Unique account number for identifying the account
    account_number = db.Column(db.String(20), unique=True, nullable=False)

    # Account balance (default to 0.00, cannot be null)
    balance = db.Column(db.Float, default=0.00, nullable=False)

    # Timestamp when the account was created
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Timestamp when the account was last updated
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Define relationship to the User model (many accounts to one user)
    user = db.relationship('User', back_populates='accounts')
