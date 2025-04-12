from app import db
from datetime import datetime

class Transaction(db.Model):
    # __tablename__ = 'transaction'

    # Primary key for the transaction
    id = db.Column(db.Integer, primary_key=True)

    # Type of transaction: e.g., 'Deposit', 'Withdrawal', 'Transfer'
    type = db.Column(db.String(20), nullable=False)

    # Transaction amount, required
    amount = db.Column(db.Float, nullable=False)

    # ID of the account sending the money (nullable for deposits)
    from_account_id = db.Column(
        db.Integer,
        db.ForeignKey('account.id'),
        nullable=True  # e.g., might be null for deposit transactions
    )

    # ID of the account receiving the money (nullable for withdrawals)
    to_account_id = db.Column(
        db.Integer,
        db.ForeignKey('account.id'),
        nullable=True  # e.g., might be null for withdrawal transactions
    )

    # Optional transaction description (e.g., "Payment for invoice #123")
    description = db.Column(db.String(255))

    # Timestamp when the transaction was created
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationship to the Account sending the transaction
    from_account = db.relationship(
        "Account",
        foreign_keys=[from_account_id],
        backref="transactions_sent"
    )

    # Relationship to the Account receiving the transaction
    to_account = db.relationship(
        "Account",
        foreign_keys=[to_account_id],
        backref="transactions_received"
    )
