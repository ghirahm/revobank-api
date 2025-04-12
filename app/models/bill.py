from app import db

class Bill(db.Model):
    # __tablename__ = 'bill'

    # Primary key for the bill record
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the User model (each bill is associated with one user)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Name of the biller (e.g., "Electricity Provider", "Internet Service")
    biller_name = db.Column(db.String(100), nullable=False)

    # Due date for the bill payment (e.g., the last day of the month)
    due_date = db.Column(db.Date, nullable=False)

    # The amount of the bill to be paid
    amount = db.Column(db.Float, nullable=False)

    # Foreign key linking to the Account model (the account used to pay the bill)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    # Relationship to the User model (backref allows access to the bill from the User model)
    user = db.relationship('User', backref='bill')

    # Relationship to the Account model (backref allows access to the bill from the Account model)
    # This assumes each bill is associated with a specific account used for payment
    account = db.relationship('Account', backref='bills')
