from app import db

class Budget(db.Model):
    # Primary key for the budget
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the User model (each budget is associated with one user)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Name of the budget (e.g., "Monthly Savings", "Holiday Fund")
    name = db.Column(db.String(100), nullable=False)

    # Total amount allocated for this budget
    amount = db.Column(db.Float, nullable=False)

    # Start date for the budget period (e.g., beginning of the month)
    start_date = db.Column(db.Date, nullable=False)

    # End date for the budget period (e.g., end of the month)
    end_date = db.Column(db.Date, nullable=False)

    # Relationship with the User model
    user = db.relationship('User', backref='budget')